def scrape_history(ticker, period='1mo', start="1980-01-01", end=pd.to_datetime('today')):
    '''
    Gets stock historical data from Yahoo Finance
    '''

    start = pd.to_datetime(start)
    period1 = int(time.mktime(datetime.datetime(start.year, start.month, start.day, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(end.year, end.month, end.day, 23, 59).timetuple()))
    interval = period # 1d, 1wk, 1mo

    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    df = pd.read_csv(query_string)
    df.index = pd.to_datetime(df['Date'])

    return df

def prices_to_returns(df):
    '''
    Converts stock prices to returns
    '''
    df['Close'] = (df['Close'].pct_change())
    df = df.get(['Close'])[1:]
    return df