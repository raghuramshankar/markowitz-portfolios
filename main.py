# %%
from src.yahoo_finance import *
if '__ipython__':
    %matplotlib widget
    %load_ext autoreload
    %autoreload 2

if __name__ == '__main__':
    tickers = 'AAPL TSLA ^GSPC'
    df = get_df(tickers)
    df = monthly_returns(df)
    results = build_capm(df['AAPL'], df['^GSPC'], plot=True)
    print(results.summary())