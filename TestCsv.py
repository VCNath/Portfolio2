import pandas as pd
from datetime import datetime, timedelta
import random

# Create a range of dates for 30 days
date_range = pd.date_range(end=datetime.now(), periods=30)

# Create a DataFrame
data = pd.DataFrame()

# Add the date_range to the DataFrame as a column
data['Date'] = date_range

# Fill the DataFrame with random data for open, high, low, close and volume
data['Open'] = [random.uniform(100, 200) for _ in range(30)]
data['High'] = [random.uniform(open_price, open_price+10) for open_price in data['Open']]
data['Low'] = [random.uniform(open_price-10, open_price) for open_price in data['Open']]
data['Close'] = [random.uniform(low, high) for low, high in zip(data['Low'], data['High'])]
data['Volume'] = [random.randint(1000, 5000) for _ in range(30)]

# Save the DataFrame to a CSV file
data.to_csv('test.csv', index=False)
