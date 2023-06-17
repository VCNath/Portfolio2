import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
import yfinance as yf
import mplfinance as mpf
# Download historical data for required stocks
data = yf.download('AAPL','2022-01-01','2023-06-01')

# Compute moving averages
data['MA10'] = data['Close'].rolling(10).mean()
data['MA30'] = data['Close'].rolling(30).mean()

# Make plot
apdict = mpf.make_addplot(data[['MA10','MA30']])
mpf.plot(data,type='candle',addplot=apdict)
