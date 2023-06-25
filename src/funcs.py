from datetime import datetime

import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import yfinance as yf
from pandas_datareader import data as pdr
import numpy as np

yf.pdr_override()


def get_t(tickers, start, end=datetime.now()):
    t = pdr.get_data_yahoo(tickers, start, end)["Close"]
    return t


def build_capm(asset, market, risk_free=pd.Series([]), plot=False):
    """
    Build Capm model for asset and market. This is a wrapper around SLS OLS to make it easier to use in tests

    Args:
        asset: pandas. Series of asset values
        market: pandas. Series of market values ( same order as asset )
        risk_free: pandas. Series of risk free values
        plot: bool whether or not to plot results on seaborn

    Returns:
        a pandas. DataFrame of capm data and a boolean that indicates if there were errors during the model
    """
    start = max(asset.index[0], market.index[0])
    asset = asset[start:]
    market = market[start:]

    if risk_free.any():
        risk_free = risk_free[start:]
        asset[0:] = asset[0:] - risk_free[0:]
        market[0:] = market[0:] - risk_free[0:]
    df_capm = asset.to_frame().join(market.to_frame())

    x_sm = sm.add_constant(market)
    y_sm = asset

    model = sm.OLS(y_sm, x_sm)
    results = model.fit()

    # Plots the capm data.
    if plot:
        sns.regplot(x=df_capm.columns[1], y=df_capm.columns[0], data=df_capm)

    return results


def monte_carlo_sim(returns, weights, mc_sims, n_days, portfolio_init):
    """
    Monte Carlo simulation of stock portfolio assuming normally distributed returns

    Args:
        returns: A time series of returns of the strategy noncumulative.
        weights: A weight vector of the strategy noncumulative.
        mc_sims: The number of Monte Carlo Simulations to run.
        n_days: The number of days to simulate.
        portfolio_init: The initial value for the portfolio.

    Returns:
        An array of simulations for the portfolio. See Also : func : ` ~mne_climate. sim_util. simulate_util `
    """
    mean_returns = returns.mean()
    cov_returns = returns.cov()

    mean_M = np.full(shape=(n_days, len(weights)), fill_value=mean_returns).T
    portfolio_sims = np.full(shape=(n_days, mc_sims), fill_value=0.0)

    L = np.linalg.cholesky(cov_returns)

    # For each m in mc_sims calculate the portfolio returns for each m.
    for m in range(0, mc_sims):
        z = np.random.normal(size=(n_days, len(weights)))
        daily_returns = mean_M + np.inner(L, z)
        portfolio_sims[:, m] = (
            np.cumprod(np.inner(weights, daily_returns.T) + 1) * portfolio_init
        )

    return portfolio_sims
