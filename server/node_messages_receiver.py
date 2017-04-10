#!/usr/bin/env python
import argparse
import json
import pika
# import codecs
import threading
import websocket

parser = argparse.ArgumentParser(description='Process message queue data to database')
parser.add_argument('mq_host',        type=str, nargs="?", default='localhost',                         help='The host of the message queue')
parser.add_argument('mq_name',        type=str, nargs="?", default='mq',                                help='The name of the message queue')
parser.add_argument('mq_user',        type=str, nargs="?", default='',                                  help='The username of the message queue')
parser.add_argument('mq_password',    type=str, nargs="?", default='',                                  help='The password of the message queue')
parser.add_argument('server_socket',  type=str, nargs="?", default='ws://localhost:5000/measurements',  help='The host of the database server')
args = parser.parse_args()

threads = []

class MessageQueueConnector():
    def __init__(self, mq_host, mq_name, mq_user, mq_password, server_socket):
        self.mq_host = mq_host
        self.mq_name = mq_name
        self.server_socket = server_socket
        self.ws = websocket.WebSocketApp(self.server_socket)
        print(self.ws)

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mq_host)
        )
        channel = connection.channel()
        
        channel.queue_declare(queue=self.mq_name)
        channel.basic_consume(self.consume, queue=self.mq_name, no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        
        def run_ws():
            while True:
                self.ws.run_forever()
                self.ws = websocket.WebSocketApp(self.server_socket)
            
        ws_thread = threading.Thread(target=run_ws, daemon=True)
        ws_thread.start()
        
        channel.start_consuming()

        
    def consume(self, ch, method, properties, body):
        print(' [x] Received {0!r}'.format(body) )
        measurements = json.loads(body.decode('utf-8'))
        try: 
            self.ws.send(json.dumps({'msg_type':'measurements', 'data': measurements}))
        except:
            pass

if __name__ == "__main__":
    connector = MessageQueueConnector(
        args.mq_host,
        args.mq_name,
        args.mq_user,
        args.mq_password,
        args.server_socket
    )
    connector.run()
