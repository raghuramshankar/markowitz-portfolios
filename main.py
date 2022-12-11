# %%
if '__ipython__':
    %matplotlib widget
    %load_ext autoreload
    %autoreload 2
from src.funcs import *

if __name__ == '__main__':
    AAPL = scrape_history('AAPL')
    AAPL = prices_to_returns(AAPL)