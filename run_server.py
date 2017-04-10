import subprocess
import signal
import sys

import socket
from gevent import monkey
monkey.patch_all()

from server import resources, app

pyro_ns_process = None

def handler(signum, frame):
    if pyro_ns_process:
        pyro_ns_process.kill()
    sys.exit()

signal.signal(signal.SIGABRT, handler)
signal.signal(signal.SIGINT, handler)

def IP ():
	return "0.0.0.0"
	# return socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    from geventwebsocket import WebSocketServer

    pyro_ns_process = subprocess.Popen (["pyro4-ns", "-n", app.config.get ('MQ_HOST')])

    WebSocketServer(
        ('0.0.0.0', 5000),
        resources
    ).serve_forever()

    node.run()
    pyro_ns_process.kill()

    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 5000), wsgi_app, handler_class=WebSocketHandler)
    # server.serve_forever()
