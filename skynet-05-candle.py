import requests
import pandas as pd
from io import StringIO

url = 'http://122.8.148.106/api/v1/data/candlestick/000/1032887?symbol=PTT&timeframe=D&startTime=2018-03-01&endTime=2018-08-18'
headers = {'X-API-KEY': '907E0507067041318FBD5248250E4EF1'}
response = requests.get(url, headers=headers)

# read text to dataframe
dataframe = pd.read_csv(StringIO(response.text),
                        names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
                        index_col='time', parse_dates=True)

print(dataframe.tail(5))