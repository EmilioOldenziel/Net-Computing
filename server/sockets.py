from __future__ import unicode_literals, division

import json
import datetime
import asyncio
import Pyro4
import socket

from geventwebsocket import WebSocketApplication

from . import app, db
from .models import Measurement, Node


async def call_remote_method(host, method, node=None):
    with Pyro4.locateNS(host=host) as ns:
        daemons = []
        for daemon, uri in ns.list (prefix = "actuator").items ():
            if node and daemon != 'actuator.' + node:
                continue
            daemons.append (Pyro4.Proxy (uri))

    for d in daemons:
        if method == 'noise':
            d.play_sound ()
        elif method == 'shutdown':
            d.shut_down ()

class MeasurementsApplication(WebSocketApplication):
    def on_message(self, message):
        if message is None:
            return
        
        message = json.loads(message)

        if message['msg_type'] == 'measurements':
            with app.app_context():
                self.process_measurements(message['data'])

        elif message['msg_type'] == 'method_call':
            with app.app_context():
                self.process_method_call(message['data'])

    def broadcast(self, data):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps(data))

    def process_measurements(self, data):
        node = Node.query.get(int(data['node_id']))
        if not node:
            return

        data['node'] = node.serialize

        for measurement in data['measurements']:
            m = Measurement(
                node=node,
                value_type=measurement['label'],
                unit=measurement['unit'],
                value=measurement['value'],
                timestamp=datetime.datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
            )
            db.session.add(m)

        db.session.commit()
        self.broadcast({
            'msg_type': 'update_clients',
            'data': data
        })

    def process_method_call(self, data):
        host = app.config.get('MQ_HOST', 'localhost')
        method = data['method']
        loop = asyncio.new_event_loop()
        if int(data['node_id']) == -1:
            loop.run_until_complete(call_remote_method(host, method))
        else:
            node = Node.query.get(int(data['node_id']))
            loop.run_until_complete(call_remote_method(host, method, node.name))

