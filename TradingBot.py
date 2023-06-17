import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors 
import time
from threading import Thread, Event
import tkinter as tk
import queue
from multiprocessing import Process, Pipe
# Data functions
def get_data(ticker, start_date, end_date, interval):
    #data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    data = pd.read_csv('test.csv', index_col=0, parse_dates=True)#leave in for testing
    return data

# Trading functions (Scalping strategy)
def scalping_strategy(data, lower_threshold, upper_threshold):
    mean_price = data['Close'].mean()
    buy_price = mean_price * (1-lower_threshold/100)
    sell_price = mean_price * (1+upper_threshold/100)
    
    if data['Close'][-1] <= buy_price:
        return 'Buy'
    elif data['Close'][-1] >= sell_price:
        return 'Sell'
    else:
        return 'Hold'
# compare data
def compare_data(short_term_data, long_term_data):
        short_term_mean = short_term_data['Close'].mean()
        long_term_mean = long_term_data['Close'].mean()
        return short_term_mean, long_term_mean
# Main function
class Bot(Thread):
    def __init__(self, tickers, queue):
        Thread.__init__(self)
        self.tickers = tickers
        self.queue = queue
        self.running = Event()
        self.running.set()
    def run(self):
        # User inputs
        #ticker = input('Enter a ticker: ').split() # Input the stock(Example: AAPL)
        while True:
            if self.running:
                for ticker in self.tickers:  
                    end_date = datetime.now()
                    start_date = end_date - timedelta(minutes=10)
                    short_term_data = get_data(ticker, start_date, end_date, interval="1m")

                    end_date_long_term = datetime.now()
                    start_date_long_term = end_date_long_term - timedelta(days=30)
                    long_term_data = get_data(ticker, start_date_long_term, end_date_long_term, interval="1d")

                    short_term_mean, long_term_mean = compare_data(short_term_data, long_term_data)
                    print(f'Short term mean for {ticker}: {short_term_mean}')
                    print(f'Long term mean for {ticker}: {long_term_mean}')
                    
                    lower_threshold = 0.03 # Adjust these parameters as per your strategy
                    upper_threshold = 0.03 # Adjust these parameters as per your strategy
                    action = scalping_strategy(short_term_data, lower_threshold, upper_threshold)
                    self.queue.put((ticker, short_term_mean, long_term_mean, short_term_data, long_term_data, action))
            time.sleep(10*60)       
    def stop(self):
        self.running.set()                
def update_gui():
    try:
        ticker, short_term_mean, long_term_mean, short_term_data, long_term_data, action = bot_queue.get(False)
        print(f'Short term mean for {ticker}: {short_term_mean}')
        print(f'Long term mean for {ticker}: {long_term_mean}')
        print(f'Ticker: {ticker}, Action: {action}')
        #create figure
        fig = plt.figure(figsize=(12,8))
        #add a subplot for the closing price
        ax1 = fig.add_subplot(211)
        ax1.set_title(f'{ticker} close price')
        ax1.set_ylabel('Price ($)')
        #plot the close price
        ax1.plot(short_term_data.index, short_term_data['Close'], label='Short term close price')
        ax1.plot(long_term_data.index, long_term_data['Close'], label='Long term close price')
        ax1.legend()
        #add a subplot for the volume
        ax2 = fig.add_subplot(212)
        ax2.set_title(f'{ticker} volume')
        ax2.set_ylabel('Volume')
        #plot the volume
        ax2.plot(short_term_data.index, short_term_data['Volume'], label='Short term volume')
        ax2.plot(long_term_data.index, long_term_data['Volume'], label='Long term volume')
        ax2.legend()
        #Interactive cursor
        mplcursors.cursor(hover=True)
         # Plot data
        plt.tight_layout()
        plt.show()
    except queue.Empty:
        pass
                    
def start_bot():
    global tickers
    tickers = ticker_entry.get().split()
    global bot_queue
    bot_queue = queue.Queue()

    global bot
    bot = Bot(tickers, bot_queue)
    bot.start()

    root.after(100, update_gui)
    
def stop_bot():
    bot.stop()
    
root = tk.Tk()
ticker_entry = tk.Entry(root)
ticker_entry.pack()

start_button = tk.Button(root, text='Start bot', command=start_bot)
start_button.pack()

stop_button = tk.Button(root, text='Stop bot', command=stop_bot)
stop_button.pack()

root.mainloop()



   