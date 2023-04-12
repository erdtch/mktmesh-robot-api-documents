from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pika
import pandas as pd
import numpy as np
import json
import crython


df = None
_7hour = 7 * 60 * 60 * 1000 * 1000000
is_buy = False
buy_bar_index = 0

@crython.job(second="*/10")
def on_cron_trigger():
    ohlc = df.reset_index().set_index('time').close.resample('1Min').ohlc().ffill()
    volume = df.reset_index().set_index('time').volume.resample('1Min').sum().ffill()

    # create OHLCV
    ohlcv = pd.concat([ohlc, volume], axis=1)
    #ohlcv = ohlcv.between_time('9:45', '17:00')

    # add bar_index field
    ohlcv['bar_index'] = np.arange(len(ohlcv))

    print(ohlcv.tail(5))
    process_strategy(ohlcv)


def process_strategy(ohlcv):
    global is_buy, buy_bar_index
    '''
    Entry:
        current close less than previous close the BUY
    Exit:
        Sell after hold for 3 bar
    StopLoss:
        None
    '''
    if not is_buy :
        print("close {}, prev-close {}".format(ohlcv.iloc[-1].close, ohlcv.iloc[-2].close))
        if ohlcv.iloc[-1].close < ohlcv.iloc[-2].close:
            is_buy = True
            buy_bar_index = ohlcv.iloc[-1].bar_index
            print('==========================')
            print("Buy at price {}, bar_index {}".format(ohlcv.iloc[-1].close, buy_bar_index))
            print('==========================')

    else:
        if ohlcv.iloc[-1].bar_index >= buy_bar_index + 3:
            print('==========================')
            print("Sell at price {}, bar_index {}".format(ohlcv.iloc[-1].close, buy_bar_index))
            print('==========================')
            is_buy = False
            buy_bar_index = 0


def on_message(channel, method_frame, header_frame, body):
    global df, _7hour
    data = body.decode("utf-8")
    print(data)
    json_body = json.loads(body)
    #time = pd.to_datetime((json_body['date'] * 1000000) + _7hour)
    time = pd.Timestamp.now()
    df = df.append(pd.DataFrame({'time': [time],
                                 'close': [float(json_body['price'])], 'volume': [float(json_body['volume'])]}),
                   ignore_index=True, sort=True)



if __name__ == '__main__':
    crython.start()

    # load historical
    df = pd.read_csv('tick.csv', names=['time', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'])

    # init rabbitmq
    credentials = pika.PlainCredentials('guest', 'guest')
    parameter = pika.ConnectionParameters(host='localhost', credentials=credentials)
    connection = pika.BlockingConnection(parameter)
    channel = connection.channel()

    result = channel.queue_declare(exclusive=True,  auto_delete=True)
    queue_name = result.method.queue
    binding_key = "realtime.tradeevent.PTT"
    channel.queue_bind(exchange='amq.topic', queue=queue_name, routing_key=binding_key)
    channel.basic_consume(on_message, queue_name, no_ack=True)

    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
