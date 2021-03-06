import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from scipy.optimize import minimize
from io import BytesIO
import base64
def dfPrepare(datalist, time_period):
    dfDict={}
    numDatalist = len(datalist)
    for i in range(numDatalist):
        dfDict[datalist[i]] = 0
    dataInUse = yf.download(tickers = datalist,
                            period=time_period , group_by = 'ticker')
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

def efficient_frontier_pre(log_re_df, num_port):
    log_re_df = log_re_df.dropna()
    n_stock = len(log_re_df.columns)

    np.random.seed(42)
    noOfportfolios = num_port
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

    return expectedReturn, expectedVolatility, sharpeRatio, weights, all_weights

def get_max_index(expected_return, expected_volatility, sharpe_ratio):
    maxindex_sr = sharpe_ratio.argmax()
    maxY = expected_return[expected_return.argmax()]
    minY = expected_return[expected_return.argmin()]
    maxX = expected_volatility[expected_volatility.argmax()]
    minX = expected_volatility[expected_volatility.argmin()]
    return maxindex_sr, maxY, minY, maxX, minX




def frontier_x_y_w(expected_return, maxindex_SR, max_ER, log_return_df_output, weights, nums_record):
    #initial setup
    n_stock = len(log_return_df_output.columns)
    
    bounds_list = [0,1]
    bounds_init = []
    for i in range(n_stock):
        bounds_init.append(tuple(bounds_list))

    bounds = tuple(bounds_init)
    init_weight = [1/n_stock] * n_stock
    #initial weighting// if n_stock , init_weight = [0.25,0.25,0.25,0.25]
    frontier_y = np.linspace(expected_return[maxindex_SR], max_ER, nums_record)
    frontier_x = []
    recommend_weighting = []
    
    #####main function
    def ret_vol_sr(weights):
        weights = np.array(weights)
        ret = np.sum(log_return_df_output.mean() * weights) * 252
        vol = np.sqrt(np.dot(weights.T, np.dot(log_return_df_output.cov()*252, weights)))
        sr = ret / vol
        return np.array([ret, vol, sr])

    def check_sum_is_one(weights):
        
    #return 0 if sum of the weights is 1
        return np.sum(weights)-1
    def minimize_volatility( weights):
        return ret_vol_sr(weights)[1]

    for i in frontier_y:
        cons = ({'type':'eq', 'fun':check_sum_is_one},
                {'type':'eq', 'fun': lambda w: ret_vol_sr(w)[0] - i})
        result = minimize(minimize_volatility, init_weight , method='SLSQP', bounds=bounds, constraints=cons)
        frontier_x.append(result['fun'])
        recommend_weighting.append(result['x'])
    return frontier_y, frontier_x, recommend_weighting

#####################
def combination_frontier(stock_list, time_period, num_ports, num_records):
    stock_df_pre = dfPrepare(stock_list, time_period)
    log_st_df = np_log_return(stock_df_pre)
    #ow = weight, aw = all weight
    eR, eV, sR, ow, aw = efficient_frontier_pre(log_st_df,  num_ports)
    max_sr, maxER, minER, maxVo, minVo = get_max_index(eR,eV,sR)
    fy, fx, rw = frontier_x_y_w(eR, max_sr, maxER, log_st_df, ow, num_records)
    return fy, fx, rw



def transform_frontier_todf(frontierY, frontierX, Weighting, stock_list):
    new_fy = np.around(frontierY, decimals=4)
    new_fx =np.around(frontierX, decimals=4)
    new_weight = np.round(Weighting, 4) *100
    frontierY_df = pd.DataFrame(new_fy, columns=['Return'])
    frontierX_df = pd.DataFrame(new_fx, columns=['Volatility'])
    recommend_weight_df = pd.DataFrame(new_weight, columns= stock_list)
    fx_fydf = pd.concat([frontierX_df, frontierY_df], axis=1)
    combined_df = pd.concat([frontierY_df, frontierX_df, recommend_weight_df], axis=1)
    
    return frontierY_df, frontierX_df,recommend_weight_df, fx_fydf, combined_df
#stock_list = ['AAPL', 'TSLA']
##
#F1, F2, RW1 = combination_frontier(stock_list)
##
#fy_df, fx_df, rw_df, fx_fydf, combindf = transform_frontier_todf(F1, F2, RW1, stock_list)
#

def json_format(res_df):
    df_json = res_df.to_json(orient="values")
    parsed = json.loads(df_json)
    result_json_df = json.dumps(parsed, indent=4)
    return result_json_df


def json_format_split(res_df):
    df_json = res_df.to_json(orient="split")
    parsed = json.loads(df_json)
    result_json_df = json.dumps(parsed, indent=4)
    return result_json_df

def json_format_record(res_df):
    df_json = res_df.to_json(orient="records")
    parsed = json.loads(df_json)
    result_json_df = json.dumps(parsed, indent=4)
    return result_json_df

def to_csv(res_df):
    res_csv = res_df.to_csv(index=False)
    return res_csv

def to_img():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_img(x,y,sr, maxindex_sr, fx,fy):
    plt.switch_backend('AGG')
    plt.figure(figsize=(12,8))
    plt.scatter(x,y, c=sr)
    plt.xlabel("Risk(Expected Volatility)")
    plt.ylabel("Return (Expected Return)")
    plt.colorbar(label="Sharpe Ratio")
    #plot the efficient frontier
    plt.scatter(x[maxindex_sr], y[maxindex_sr],c='red')
    plt.plot(fx,fy, 'r--', linewidth=3)
    plt.tight_layout()
    chart = to_img()
    return chart
#stock_list = ['AAPL', 'TSLA','GME']
###
#stock_df_pre = dfPrepare(stock_list)
#log_st_df = np_log_return(stock_df_pre)
#eR, eV, sR, ow, aw = efficient_frontier_pre(log_st_df)
#max_sr, maxER, minER, maxVo, minVo = get_max_index(eR,eV,sR)
#fy, fx, rw = frontier_test(eR, max_sr, maxER, log_st_df, ow)
#to_img(eV, eR, sR, max_sr ,fx,fy)
