from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Stock
from .forms import StockForm
import requests 
import json
# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html', {})
    
def iex_stock_data(ticker_symbol):
    API_token = settings.IEX_API_TOKEN    
    url = "https://cloud.iexapis.com/stable/stock/" + ticker_symbol + "/quote?token=" +API_token

    try:
        stock_data = requests.get(url)
        if stock_data.status_code == 200:
            stock_data = json.loads(stock_data.content)
        else:
           stock_data = {'Error': 'There was a problem in stock ticker !'}
    except Exception as e:
       stock_data = {'Error':'Please try again later.'}
    return stock_data

def search_stock_data(request):
    API_token = settings.IEX_API_TOKEN
    
    if request.method == 'POST':
        ticker = request.POST['ticker']
        # pk_d7d6fe0afa014e21a15addd0105fd7c6
        stockData = iex_stock_data(ticker)
    return render(request, 'quotes/search_stock.html', {'stock_data': stockData})


def search_batch_stockdata(stock_tickers):
    datalist = []
    try:
        token = settings.sandbox_IEX_API_token
        url = 'https://sandbox.iexapis.com/stable/stock/market/batch?symbols=' + stock_tickers + '&types=quote&token=' + token
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
            for item in data:
                datalist.append(data[item]['quote'])
                ##THE JSON FILE FORMAT
                ####STOCK_TICKER
                ####### quote
                ########## STOCK_TICKER_DATA
        else:
            data = {'Error': 'There are errors, please try again.'}
    except Exception as e:
        data = {'Error': 'Connection Error! Please try again!'}
    return data_list



def check_valid_stock(ticker_symbol):
    stockValid = iex_stock_data(ticker_symbol)
    if 'Error' not in stockValid:
        return True
    else:
        return False

def check_stock_inDB(ticker_symbol):
    try:
        stock = Stock.objects.get(ticker=ticker_symbol)
        if stock:
            return True
    except Exception:
        return False

def stock_data_batch(stock_tickers):
    stock_list = []
    token = settings.SANDBOX_IEX_API_TOKEN

    url = 'https://sandbox.iexapis.com/stable/stock/market/batch?symbols=' + stock_tickers + '&types=quote&token=' + token
    try:
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
            for item in data:
                stock_list.append(data[item]['quote'])
        else:
            data = {'Error' : 'There is an error !'}
    except Exception as e:
        data = {'Error': 'There is an error in connection!'}
    
    return stock_list


    #else:
    #    context = {}
    #    stockdata = Stock.objects.all()
        
    #    if stockdata:
    #        ticker_list = [stock.ticker for stock in stockdata]
    #        ticker_list = list(set(ticker_list))
    #        tickers = ','.join(ticker_list)
    #        stockdata1 = stock_data_batch(tickers)
    #        
    #        return render(request, 'quotes/add_stock.html', {'stockdata': stockdata1})
    #    else:
    #        messages.info(request, 'You dont have any stock in your portfolio!')
    #        return render(request, 'quotes/add_stock.html')
        
        #return render(request, 'add_stock.html', {'stockdata': stockdata})   
def existing_stock(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        if ticker:
            form = StockForm(request.POST or None)

            if form.is_valid():
  
                if check_stock_inDB(ticker):
                    messages.warning(request, "Stock is already existed in portfolio!")
                    return redirect('quotes:existing_stock')
                    
                if check_valid_stock(ticker):
                    form.save() #if it is valid, save it in database.
                    messages.success(request, ("Stock has been Added"))
                    return redirect('quotes:existing_stock')
        
        messages.warning(request,'Please enter a valid ticker name!')
        return redirect('quotes:existing_stock')
    else:
        stockdata = Stock.objects.all()

        if stockdata:
            ticker_list = [stock.ticker for stock in stockdata]
            ticker_list = list(set(ticker_list))
            tickers = ','.join(ticker_list)
            stockdata1 = stock_data_batch(tickers)
            return render(request, 'quotes/add_stock.html', {'stockdata': stockdata1})     
        else:
            messages.info(request, 'You dont have any stock in your portfolio!')
        return render(request, 'quotes/add_stock.html')
                
                
        
#return render(request, 'add_stock.html', {'stockdata':stockdata})

def portfolio(request):
    ticker = Stock.objects.all()
    
    return render(request, 'quotes/portfolio.html',{'ticker':ticker})

def delete(request, stock_symbol): #### replace stock_ticker as stock_id.
    item = Stock.objects.get(ticker=stock_symbol)
    #item = Stock.objects.get(pk=stock_id) # primary key = stock id
    item.delete()
    messages.success(request, ("Stock has been deleted !"))

    return redirect('quotes:existing_stock') #after delete -> still in add_stock page

#def delete(request, stock_id):
#    item = Stock.objects.get(pk= stock_id) # primary key = stock id
#    item.delete()
#    messages.success(request, ("Stock has been deleted !"))

#    return redirect(add_stock) #after delete -> still in add_stock page
#
#
#
#