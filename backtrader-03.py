import backtrader as bt
import pandas as pd

# back trader with indicator plot
class St(bt.Strategy):
    def __init__(self):
        bt.indicators.SimpleMovingAverage(self.data, period=10)
        bt.indicators.SimpleMovingAverage(self.data, period=20)
        bt.indicators.SimpleMovingAverage(self.data, period=30)

        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])


# Create a Data Feed
df = pd.read_csv('candlestick.csv', names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
                 index_col='time', parse_dates=True)
data = bt.feeds.PandasData(dataname=df)
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run(stdstats=False)
cerebro.plot(style='bar')
