import yfinance as yf
import pandas as pd
import time
from datetime import datetime

ticker_symbol = 'GC=F'

df = pd.DataFrame(columns=['timestamp','price'])

#fetch stock price

try:
    while True:
        ticker = yf.Ticker(ticker_symbol)
        ticker_info = ticker.info

        if 'regularMarketPrice' in ticker_info:
            price = ticker_info['regularMarketPrice']
            timestamp = datetime.now()
            print(f"{timestamp}: The current price of {ticker_symbol} is {price}")

            df = df.append({'timestamp': timestamp, 'price': price}, ignore_index=True)
        else:
            print(f"Could not fetch the price for {ticker_symbol} at {datetime.now()}")

        time.sleep(60)
except KeyboardInterrupt:
    print("Stopped.")



df.to_csv('real_time_stock_data.csv', index=False)

