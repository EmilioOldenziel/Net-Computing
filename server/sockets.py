from __future__ import unicode_literals, division

import json

from geventwebsocket import WebSocketApplication

from . import app, db
from .models import Measurement

class MeasurementsApplication(WebSocketApplication):
    def on_message(self, message):
        if message is None:
            return

        app.app_context()
        
        message = json.loads(message)

        if message['msg_type'] == 'measurements':
            self.process_measurements(message['data'])

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
