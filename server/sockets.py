from __future__ import unicode_literals, division

import json
import asyncio
import Pyro4
import socket

from geventwebsocket import WebSocketApplication

from . import app, db
from .models import Measurement

def IP ():
    return socket.gethostbyname(socket.gethostname())

async def call_remote_method(host, method):
    with Pyro4.locateNS(host=host) as ns:
        daemons = [Pyro4.Proxy (uri) for d, uri in ns.list(prefix = "actuator").items()]

    for d in daemons:
        if method == 'noise':
            d.play_sound ()
        elif method == 'shutdown':
            d.shut_down ()


class MeasurementsApplication(WebSocketApplication):
    def on_message(self, message):
        if message is None:
            return

        app.app_context()
        
        message = json.loads(message)

        if message['msg_type'] == 'measurements':
            self.process_measurements(message['data'])

        elif message['msg_type'] == 'method_call':
            host = IP ()
            method = message['data']['method']
            loop = asyncio.new_event_loop()
            loop.run_until_complete(call_remote_method(host, method))

    def broadcast(self, data):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps(data))

    def process_measurements(self, data):
        for measurement in data['measurements']:
            m = Measurement(
                value_type=measurement['label'],
                unit=measurement['unit'],
                value=measurement['value']
            )
            db.session.add(m)
        db.session.commit()
        self.broadcast({
            'msg_type': 'update_clients',
            'data': data['measurements']
        })
