from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from quotes.models import Position
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


def portfolio_dashboard(request):
    user_holding = Position.objects.filter(created_by = request.user)
    
    return render(request, 'portfolio/dashboard.html')


def efficient_frontier_select(request):
    user_holding = Position.objects.filter(created_by = request.user)
    
    context = {
        'holding': user_holding
    }
    return render(request, 'portfolio/efficient_frontier.html', context)


def efficient_frontier_post(request):
    if request.method == 'POST':
        print(request.POST)
        selected_stocklist = request.POST.getlist('stock_symbol')
        #if checkbox --> ['AAPL', 'ARKK']
        #selected_stocklist  -->['AAPL', 'ARKK']
        print(selected_stocklist)
        
        
    return JsonResponse(request.POST)

#def efficient_fronter(datalist):

