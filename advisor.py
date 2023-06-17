import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

data = pd.read_csv('/Users/nathanielvc/Downloads/archive(9)/data.csv')

print(data.head())
