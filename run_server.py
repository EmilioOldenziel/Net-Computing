from gevent import monkey
monkey.patch_all()

from server import resources

if __name__ == '__main__':
    from geventwebsocket import WebSocketServer

    WebSocketServer(
        ('0.0.0.0', 5000),
        resources
    ).serve_forever()

    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 5000), wsgi_app, handler_class=WebSocketHandler)
    # server.serve_forever()
