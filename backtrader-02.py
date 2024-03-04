import pandas as pd
from io import StringIO
import requests

# Import the backtrader platform
import backtrader as bt


# Create a cerebro entity
cerebro = bt.Cerebro()

# Create a Data Feed
dataframe = pd.read_csv('candlestick.csv', names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
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