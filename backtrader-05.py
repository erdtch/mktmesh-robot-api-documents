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
    params = (('holding_bar', 0),)
    has_order = False
    bar_index = 0
    bar_executed = 0

    def next(self):
        date = self.datas[0].datetime.date(0)
        close = self.datas[0].close[0]

        self.bar_index += 1
        print('%s Price = %.2f, bar_index = %d, bar_executed = %d' % (date, close, self.bar_index, self.bar_executed))

        if not self.has_order:
            if self.datas[0].close[0] < self.datas[0].close[-1]:
                #if self.datas[0].close[-1] < self.datas[0].close[-2]:
                print('%s Buy %.2f at %d' % (date, close, self.bar_index))
                self.buy()
                self.bar_executed = self.bar_index
                self.has_order = True

        else:
            if self.bar_index > self.bar_executed + self.params.holding_bar :
                print('%s Sell, %.2f at %d' % (date, close, self.bar_index))
                self.sell()
                self.has_order = False



if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    df = pd.read_csv('AOT.csv', names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
                     index_col='time', parse_dates=True)
    data = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy, holding_bar = 5)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.SizerFix, stake=10000)
    cerebro.broker.setcommission(commission=0.157 / 100)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()