import pandas as pd
import numpy as np
import time
import datetime

def scrapeHistory(ticker, interval='1d', start=pd.to_datetime("1980-01-01"), end=pd.to_datetime('today')):

    '''gets stock historical data from Yahoo Finance'''
    '''credit: https://learndataanalysis.org/source-code-download-historical-stock-data-from-yahoo-finance-using-python/'''

    '''define start and end periods'''
    period1 = int(time.mktime(datetime.datetime(start.year, start.month, start.day, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(end.year, end.month, end.day, 23, 59).timetuple()))
    interval = '1d' # 1d, 1w, 1m

    '''create query string to web scrape'''
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    '''store in pandas df'''
    df = pd.read_csv(query_string)
    df.index = pd.to_datetime(df["Date"])
    return df