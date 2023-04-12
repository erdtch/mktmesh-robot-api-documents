import pika
import json
import pandas as pd

def on_message(channel, method_frame, header_frame, body):
    json_body = json.loads(body)
    print("symbol {}, price {}".format(json_body['symbol'], json_body['price']))


credentials = pika.PlainCredentials('X-API-KEY:XXXXXXX', '')
parameter = pika.ConnectionParameters(host='122.8.148.106', credentials=credentials)
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