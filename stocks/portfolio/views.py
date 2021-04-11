from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from quotes.models import Position
from account.models import Account
from . import utils as ef
from .forms import SaveEfficientFrontierForm
from .models import Portfolio
from .processimg import get_ef_image
import requests 
import json

# Create your views here.
#plotly



def home(request):
    
    return render(request, 'portfolio/home.html')

def get_latest_price(stock_symbol):
    API_token = settings.IEX_API_TOKEN
    url = "https://cloud.iexapis.com/stable/stock/" + stock_symbol + "/quote?token=" +API_token
    try:
        stock_data = requests.get(url)

        if stock_data.status_code == 200:
            stock_data = json.loads(stock_data.content)
    except Exception as e:
        stock_data = {'Error': 'Please try again later!'}
    
    return stock_data

def get_batch_stock_price(stock_tickers):
    stocklist = []
    token = settings.SANDBOX_IEX_API_TOKEN
    url = 'https://sandbox.iexapis.com/stable/stock/market/batch?symbols=' + stock_tickers + '&types=quote&token=' + token
    try:
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
            
                ##THE JSON FILE FORMAT
                ####STOCK_TICKER
                ####### quote
                ########## STOCK_TICKER_DATA
            
        else:
            data = {'Error': 'There are errors, please try again.'}
    except Exception as e:
        data = {'Error': 'Connection Error! Please try again!'}
    return data



@login_required
def portfolio_overview(request):
    user_holding = Position.objects.filter(created_by = request.user)
    
    
    test_holding_dict = Position.objects.filter(created_by = request.user).values()
    stock_symbol_list = [stock.stock_symbol for stock in user_holding]
    stock_symbol_list = list(set(stock_symbol_list))
    stock_symbols = ','.join(stock_symbol_list)
    stockdata1 = get_batch_stock_price(stock_symbols)
    
    # --> AMD
    #print(test_holding_dict)
    #<QuerySet [{'id': 1, 'stock_symbol': 'AAPL', 'stock_shares': 1, 'stock_price': 0.0, 'created_by_id': 1}, 
    # {'id': 4, 'stock_symbol': 'TSLA', 'stock_shares': 1, 'stock_price': 0.0, 'created_by_id': 1}, 
    # {'id': 5, 'stock_symbol': 'GME', 'stock_shares': 4, 'stock_price': 0.0, 'created_by_id': 1}, 
    # {'id': 10, 'stock_symbol': 'AMD', 'stock_shares': 1, 'stock_price': 50.0, 'created_by_id': 1}]>
    for i in test_holding_dict:
        stockSymbol = i['stock_symbol']
        i['stock_latestprice'] = stockdata1[stockSymbol]['quote']['latestPrice']
        
    test_list = list(test_holding_dict)
    
    #print(stockdata1)
    #print(user_portfolio['AAPL']['id']) --->1
    
        #---> 1,4,5,10
    context = {
        'portfolio': test_list

    }
    
    return render(request, 'portfolio/overview.html', context)

def delete(request, stock_symbol):
    item = Position.objects.filter(created_by = request.user, stock_symbol= stock_symbol)
    item.delete()
    messages.success(request, ("Stock has been deleted !"))
    return redirect('portfolio:overview')

def portfolio_dashboard(request):
    user_holding = Position.objects.filter(created_by = request.user)
    
    return render(request, 'portfolio/dashboard.html')

@login_required
def efficient_frontier_select(request):
    user_holding = Position.objects.filter(created_by = request.user)
    selected_stock = None
    #ta = None
    #tb = None
    #tc = None
    ef_df = None
    json_df = None
    fy_json = None
    fx_json = None
    w_df_json = None
    fxfy_json = None
    ef_df_html = None
    efdf_json = None
    list_efdf = None
    efdf_split = None
    fxfy_record = None
    w_df_split = None
    test_chart = None
    save_ef_form = None
    if request.method == 'POST':
        selected_stock = request.POST.getlist('stock_symbol')
        ta, tb, tc = ef.combination_frontier(selected_stock)
        fy_df, fx_df, w_df, fxfy_df, ef_df = ef.transform_frontier_todf(ta,tb,tc, selected_stock)
        fy_json = ef.json_format(fy_df)
        fx_json = ef.json_format(fx_df)
        #w_df_json = ef.json_format(w_df)
        #fxfy_json = json.loads(ef.json_format(fxfy_df))
        #efdf_json = ef.json_format(ef_df)
        ef_df_html = ef_df.to_html()
        #list_efdf = json.loads(efdf_json)
        #efdf_split = json.loads(ef.json_format_split(ef_df))
        fxfy_record = json.loads(ef.json_format_record(fxfy_df))
        w_df_split = json.loads(ef.json_format_split(w_df))
        #print(list_efdf)
        #print(type(list_efdf))
        
        ###output the image of EF
        stock_df_pre = ef.dfPrepare(selected_stock)
        log_st_df = ef.np_log_return(stock_df_pre)
        eR, eV, sR, ow, aw = ef.efficient_frontier_pre(log_st_df)
        max_sr, maxER, minER, maxVo, minVo = ef.get_max_index(eR,eV,sR)
        fy, fx, rw = ef.frontier_test(eR, max_sr, maxER, log_st_df, ow)
        test_chart = ef.get_img(eV, eR, sR, max_sr ,fx,fy)

        save_ef_form = SaveEfficientFrontierForm(initial={'name':selected_stock
            ,'description':selected_stock})
        
    context = {
        'holding': user_holding,
        'selected_stock': selected_stock,
        'frontier_y': fy_json,
        'frontier_x': fx_json,
        'recommend_weighting':w_df_json,
        'fxfy': fxfy_json,
        'df':ef_df_html,
        'efdf': efdf_json,
        'array_efdf':list_efdf,
        'efdf_split' : efdf_split,
        'fxfy_record' : fxfy_record,
        'w_df_split' : w_df_split,
        'test_chart': test_chart,
        'efform': save_ef_form
    }
    
    return render(request, 'portfolio/efficient_frontier.html', context)

def save_in_portfolio(request):
    
    
    if request.is_ajax():
        name = request.POST.get('save_name')
        description = request.POST.get('save_descr')
        image = request.POST.get('image')
        user_id = request.user.id
        user_obj = Account.objects.get(username = request.user)
        img = get_ef_image(image)
        try:
            Portfolio.objects.create(name=name, image=img, description=description, created_by=user_obj)
            data = {'success' : 'Saved!'}
        except:
            data = {'fail': 'Try again later!'}
            
    return JsonResponse(data)
    

def efficient_frontier_post(request):
    if request.method == 'POST':
        print(request.POST)
        selected_stocklist = request.POST.getlist('stock_symbol')
        #if checkbox --> ['AAPL', 'ARKK']
        #selected_stocklist  -->['AAPL', 'ARKK']
        print(selected_stocklist)
        
        
    return JsonResponse(request.POST)

#def efficient_fronter(datalist):

