import pandas as pd
from io import StringIO
import requests

# Import the backtrader platform
import backtrader as bt


# Create a cerebro entity
cerebro = bt.Cerebro()

# real url content with key
url = 'http://122.8.148.106/api/v1/data/candlestick/000/1032887/?symbol=PTT&timeframe=D&startTime=2018-03-01&endTime=2018-08-18'
headers = {'X-API-KEY': '907E0507067041318FBD5248250E4EF1'}
response = requests.get(url, headers=headers)
data = response.text

# read text to dataframe
dataframe = pd.read_csv(StringIO(data), names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
                        index_col='time', parse_dates=True)
# Create a Data Feed
data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)
cerebro.broker.setcash(1000000.0)
cerebro.addsizer(bt.sizers.SizerFix, stake=10000)
cerebro.broker.setcommission(commission=0.157/100)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run(stdstats=False)
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style='candlestick')