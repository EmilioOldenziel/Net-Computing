#!/usr/bin/env python
import pika, json


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='mq')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    measurement_dict = json.loads(body)
    # insert dict into database as measurement

channel.basic_consume(callback,
                      queue='mq',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()