from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd

# Import the backtrader platform
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):
    def next(self):
        date = self.datas[0].datetime.date(0)
        close = self.datas[0].close[0]
        print('%s Price, %.2f' % (date, close))

        if self.datas[0].close[0] < self.datas[0].close[-1]:
            if self.datas[0].close[-1] < self.datas[0].close[-2]:
                print('%s Buy, %.2f' % (date, close))
                self.buy()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    df = pd.read_csv('candlestick.csv', names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
                     index_col='time', parse_dates=True)
    data = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.SizerFix, stake=10000)
    cerebro.broker.setcommission(commission=0.157 / 100)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style='bar')