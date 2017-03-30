import Pyro4
import socket

def IP ():
	# return socket.gethostbyname(socket.gethostname())
    # return '145.97.135.165'
    return 'localhost'

daemons = []
with Pyro4.locateNS (host = IP ()) as ns:
	for daemon, uri in ns.list (prefix = "actuator").items ():
		print ("Found an actuator: {0}".format (daemon))
		daemons.append (Pyro4.Proxy (uri))

for d in daemons:
	d.shut_down ()

