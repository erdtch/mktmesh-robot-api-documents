import backtrader as bt
import pandas as pd


class SmaCross(bt.SignalStrategy):
    params = (('pfast', 0), ('pslow', 0),)

    def __init__(self):
        self.startcash = self.broker.getvalue()
        sma1 = bt.ind.SMA(period=self.params.pfast)
        sma2 = bt.ind.SMA(period=self.params.pslow)
        self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma1, sma2))

    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash, 2)
        print('{}\t{}\t{}'
              .format(self.params.pfast, self.params.pslow, pnl))



if __name__ == '__main__':
    # Create a Data Feed
    df = pd.read_csv('AOT.csv', names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
                     index_col='time', parse_dates=True)

    #df = df.tail(200)
    data = bt.feeds.PandasData(dataname=df)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    #cerebro.addstrategy(SmaCross)
    cerebro.optstrategy(SmaCross,  pfast=range(5,20), pslow=range(20,50))

    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.SizerFix, stake=10000)
    cerebro.broker.setcommission(commission=0.157/100)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
