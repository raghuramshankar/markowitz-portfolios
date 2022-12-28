# %%
import re

import requests


def get_tickers():
    master_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    master_data = requests.get(master_url, allow_redirects=False)
    nyse_tickers = re.findall(
        r"(?<=https://www.nyse.com/quote/XNYS:).+?(?=\">)", master_data.text
    )
    nasdaq_tickers = re.findall(
        r"(?<=http://www.nasdaq.com/symbol/).+?(?=\">)", master_data.text
    )
    return nyse_tickers, nasdaq_tickers
