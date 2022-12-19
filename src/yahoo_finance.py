# %%
from datetime import datetime

import pandas_datareader.data as reader
import statsmodels.api as sm
import yfinance as yf
import pandas as pd
import seaborn as sns

def get_df(tickers, end=datetime.now(), start=5):
    '''
    returns a yf dataframe with data for the stickers
    inputs:
        end: end date in datetime format
        start: number of years to look back on from today
        tickers: tickers as a single string with spaces
    outputs:
        df: yf dataframe
    '''
    start = datetime(end.year - start, end.month, end.day)
    df = yf.download(tickers, start=datetime.strftime(start,format='%Y-%m-%d'), end=datetime.strftime(end, '%Y-%m-%d'))['Adj Close']
    df.columns = tickers.split(' ')
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    
    return df

def monthly_returns(df):
    '''
    returns the monthly returns of yf dataframe/series
    input:
        df: yf dataframe/series
    output:
        df: yf dataframe/series
    '''

    df = df.resample('M').ffill().pct_change().dropna(axis=0)
    return df

def build_capm(asset, market, plot=False):
    '''
    builds the CAPM regression model for the input tickers from the start to end date
    inputs:
        asset: yf dataframe with monthly returns of asset
        marketL yf dataframe with monthly returns of market
    outputs:
        results:results object with CAPM model
    '''
    # make the dfs uniform
    start = max(asset.index[0], market.index[0])
    asset = asset[start:]
    market = market[start:]
    df = pd.DataFrame({asset.name: asset, market.name: market})

    # add bias term to x axis
    x_sm = sm.add_constant(market)
    y_sm = asset
    
    # fit the CAPM model
    model = sm.OLS(y_sm, x_sm)
    results = model.fit()

    # plot
    if plot:
        sns.regplot(x=df.columns[1], y=df.columns[0], data=df)

    return results