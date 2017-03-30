#!/usr/bin/env python
import argparse
import json
import pika

from websocket import create_connection


parser = argparse.ArgumentParser(description='Process message queue data to database')
parser.add_argument('mq_host',                type=str, nargs="?", default='localhost',                  help='The host of the message queue')
parser.add_argument('server_socket',            type=str, nargs="?", default='ws://localhost:5000/measurements',      help='The host of the database server')
args = parser.parse_args()


class MessageQueueConnector():
    def __init__(self, mq_host, server_socket):
        self.mq_host = mq_host
        self.server_socket = server_socket

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mq_host)
        )
        channel = connection.channel()
        
        channel.queue_declare(queue='mq')
        channel.basic_consume(self.consume, queue='mq', no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        
    def consume(self, ch, method, properties, body):
        print(' [x] Received {0!r}'.format(body) )
        measurements = json.loads(body)
        try: 
            ws = create_connection(self.server_socket)
            ws.send(json.dumps({'msg_type':'measurements', 'data': measurements}))
            ws.close()
        except:
            return

if __name__ == "__main__":
    connector = MessageQueueConnector(args.mq_host, args.server_socket)
    connector.run()
