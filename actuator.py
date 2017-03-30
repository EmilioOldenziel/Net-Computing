import os
import socket
import Pyro4        # RMI

def IP ():
	return socket.gethostbyname(socket.gethostname())

@Pyro4.expose                               # Expose this class to RMI
@Pyro4.behavior(instance_mode="single")     # Single instance per node
class Actuator:
	# Define methods here to be accessible remotely.
	def shut_down (self):
		os.system ("shutdown -h now")


	# Starts the pyro daemon
	def start (self):
		Pyro4.Daemon.serveSimple(
			{
				Actuator: "actuator"
			},
			host = IP (),
			ns = True
			)

def main ():
	actuator = Actuator ()
	actuator.start ()

if __name__ == "__main__":
	main ()
