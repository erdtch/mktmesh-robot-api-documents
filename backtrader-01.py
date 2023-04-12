import backtrader as bt


cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000.0)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())