#!/usr/bin/env python
import pika, json
from . import app, db
from .models import Node, Sensor


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='Nodes')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    measurement_dict = json.loads(body)
    # insert dict into database as measurement

channel.basic_consume(callback,
                      queue='Nodes',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()