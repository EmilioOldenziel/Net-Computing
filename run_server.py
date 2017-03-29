import Pyro4.naming
import socket
from server import app

def IP ():
	return socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
	uri, daemon, bcast_server = Pyro4.naming.startNS (
		host = IP (), 
		port = 0,
		enableBroadcast = False)
		# bcport = 0
		# )
	print ("Name server started at {0}".format (uri))

	app.debug = True
	app.run (host = IP ())
