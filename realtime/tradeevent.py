import pika
import json
import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def on_message(channel, method_frame, header_frame, body):
    data = body.decode("utf-8")
    json_body = json.loads(body)
    print(json_body)


if __name__ == '__main__':
    # init rabbitmq
    # Username: X-API-KEY:<BROKER CODE>:<API KEY>
    # Password: accountNo
    credentials = pika.PlainCredentials('X-API-KEY:900:1AFD14813B4EC7AC52FF93B380FAB2891', '1032887')
    parameter = pika.ConnectionParameters(host='122.8.148.106', credentials=credentials)
    connection = pika.BlockingConnection(parameter)
    channel = connection.channel()

    queue_name = 'py-trade-event-' + get_random_string(8)
    channel.queue_declare(exclusive=True, auto_delete=True, queue=queue_name)

    binding_key = "realtime.tradeevent.PTT"
    channel.queue_bind(exchange='amq.topic', queue=queue_name, routing_key=binding_key)
    channel.basic_consume(queue_name, on_message, auto_ack=True)

    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
