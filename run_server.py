import Pyro4.naming
import socket
from server import app

def IP ():
	return socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
	app.debug = True
	app.run (host = IP ())
