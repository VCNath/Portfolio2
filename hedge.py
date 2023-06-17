import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

#define a function that downloads stock data
def download_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    data = yf.download(tickers, start=start_date, end=end_date)
    if data is None:
        print("Failed to download data")
        return None
    if data.empty:
        print("Downloaded data is empty")
        return None
    return data['Adj Close']

    
#define a function that finds the best hedge    
def find_best_hedge(portfolio: List[str], stocks: List[str], start_date: str, end_date: str) -> str:
    data = download_data(portfolio + stocks, start_date, end_date)

    print(f"Data columns: {data.columns}")  # print the column names of data

    for ticker in portfolio:
        if ticker not in data.columns:
            print(f"{ticker} not found in data")
    
    # Now calculate portfolio returns
    try:
        portfolio_returns = data[portfolio].mean(axis=1).pct_change()
    except Exception as e:
        print(f"Error while calculating portfolio returns: {e}")
        return None

    correlations = {}
    for stock in stocks:
        stock_returns = data[stock].pct_change()
        correlation = portfolio_returns.corr(stock_returns)
        correlations[stock] = correlation

    best_hedge = min(correlations, key=correlations.get)

    return best_hedge
def plot_prices(data: pd.DataFrame, stocks: List[str]):
    data[stocks].plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted closing price")
    plt.title("stock Price over time")
    plt.legend(stocks)
    plt.show()
# Test the function
portfolio = ['AAPL', 'MSFT', 'TSLA']
stocks = ['SPY', 'QQQ', 'IWM', 'EEM', 'EFA', 'GLD', 'SLV', 'USO', 'HYG', 'LQD', 'TLT', 'VNQ','^GSPC']

best_hedge = find_best_hedge(portfolio, stocks, '2020-01-01', '2023-01-01')
print(f'the best hedge is {best_hedge}')

data = download_data(portfolio + [best_hedge], '2020-01-01', '2023-01-01')
plot_prices(data, portfolio + [best_hedge])

