import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from scipy.optimize import minimize

def dfPrepare(datalist):
    dfDict={}
    numDatalist = len(datalist)
    for i in range(numDatalist):
        dfDict[datalist[i]] = 0
    dataInUse = yf.download(tickers = datalist,
                            period="1y", group_by = 'ticker')
    if numDatalist != 1:
        for i in dfDict:
            dfDict[i] = pd.DataFrame({str(i): dataInUse[i]["Adj Close"]})
    else:
        for i in dfDict:
            dfDict[i] = pd.DataFrame({str(i): dataInUse["Adj Close"]})
    df_readyconcat = []
    for i in datalist:
        df_readyconcat.append(dfDict[i])
    total_df1 = pd.concat(df_readyconcat,axis=1)
    total_df1.columns = datalist
    
    return total_df1

def np_log_return(stockDF):
    log_ret = np.log(stockDF/stockDF.shift(1))
    return log_ret

def efficient_frontier_pre(log_re_df):
    log_re_df = log_re_df.dropna()
    n_stock = len(log_re_df.columns)

    np.random.seed(42)
    noOfportfolios = 1000
    all_weights = np.zeros((noOfportfolios,n_stock))

    expectedReturn = np.zeros(noOfportfolios)
    expectedVolatility = np.zeros(noOfportfolios)
    sharpeRatio = np.zeros(noOfportfolios)

    riskfree_R = 0.93/100
    #mean_log_return = log_return_df.mean()
    #sigma = log_return_df.cov()

    for i in range(noOfportfolios):
        weights = np.array(np.random.random(n_stock))
        weights = weights/np.sum(weights)
    
    #Save weights
    
        all_weights[i,:] = weights
        
        expectedReturn[i] = np.sum((log_re_df.mean()* 252 * weights))
        expectedVolatility[i] = np.sqrt(np.dot(weights.T, np.dot(log_re_df.cov()* 252,weights)))
        
        sharpeRatio[i] = (expectedReturn[i] - riskfree_R)/expectedVolatility[i]

    return expectedReturn, expectedVolatility, sharpeRatio, weights

def get_max_index(expected_return, expected_volatility, sharpe_ratio):
    maxindex_sr = sharpe_ratio.argmax()
    maxY = expected_return[expected_return.argmax()]
    minY = expected_return[expected_return.argmin()]
    maxX = expected_return[expected_volatility.argmax()]
    minX = expected_return[expected_volatility.argmin()]
    return maxindex_sr, maxY, minY, maxX, minX

def get_ret_vol_sr(log_return_df_output, weights):
    weights = np.array(weights)
    ret = np.sum(log_return_df_output.mean() * weights) * 252
    vol = np.sqrt(np.dot(weights.T, np.dot(log_return_df_output.cov()*252, weights)))
    sr = ret / vol
    return np.array([ret, vol, sr])


def neg_sharpe(weights):
# the number 2 is the sharpe ratio index from the get_ret_vol_sr
    return get_ret_vol_sr(log_st_df, weights)[2] * -1

def check_sum(weights):
    
    #return 0 if sum of the weights is 1
    return np.sum(weights)-1

def minimize_ef(log_return_df_output, weights_output):
    
    get_ret_vol_sr_result = get_ret_vol_sr(log_st_df, w1)

    n_stock = len(log_return_df_output.columns)
    cons = ({'type':'eq', 'fun':check_sum})
    bounds_list = [0,1]
    bounds_init = []
    for i in range(n_stock):
        bounds_init.append(tuple(bounds_list))

    bounds = tuple(bounds_init)
    #setup initial weighting ---> 1 / numbers of stock
    #if 3 stocks, weighting -> 0.33 each (1/3)
    init_weight = [1/n_stock] * n_stock
    
    optim_result = minimize(neg_sharpe, init_weight, method='SLSQP', bounds=bounds, constraints=cons)

    return optim_result

def minimize_volatility(weights):
    
    return get_ret_vol_sr(log_st_df, weights)[1]
    
def frontier_x_y(expected_return, maxindex_SR, max_ER, log_return_df_output, weights_output):
    n_stock = len(log_return_df_output.columns)
    bounds_list = [0,1]
    bounds_init = []
    for i in range(n_stock):
        bounds_init.append(tuple(bounds_list))

    bounds = tuple(bounds_init)
    #setup initial weighting ---> 1 / numbers of stock
    #if 3 stocks, weighting -> 0.33 each (1/3)
    init_weight = [1/n_stock] * n_stock
    frontier_y = np.linspace(expected_return[maxindex_SR], max_ER, 50)
    frontier_x = []
    recommend_weighting = []
    for i in frontier_y:
        cons = ({'type':'eq', 'fun':check_sum},
                {'type':'eq', 'fun': lambda w: get_ret_vol_sr(log_return_df_output, w)[0] - i})
        result = minimize(minimize_volatility,init_weight,method='SLSQP', bounds=bounds, constraints=cons)
        frontier_x.append(result['fun'])
        recommend_weighting.append(result['x'])
    return frontier_y, frontier_x, recommend_weighting

stock_list = ['AAPL', 'TSLA', 'GME']
stock_df_pre = dfPrepare(stock_list)
log_st_df = np_log_return(stock_df_pre)

eR, eV, sR, w1 = efficient_frontier_pre(log_st_df)
maxSR, maxER, minER, maxEV, minEV = get_max_index(eR,eV,sR)
FY, FX, RW = frontier_x_y(eR, maxSR, maxER, log_st_df, w1)

plt.figure(figsize=(12,8))
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.scatter(eV,eR, c=sR)
plt.colorbar(label='Sharpe Ratio')
plt.scatter(eV[maxSR], eR[maxSR],c='red')
plt.plot(FX,FY, 'r--', linewidth=3)
#plt.savefig('cover.png')
plt.show()
opt = minimize_ef(log_st_df, w1)
print(opt)