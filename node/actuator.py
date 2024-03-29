import argparse
import os
import sys
import socket
import Pyro4        # RMI

if sys.platform.startswith('win32'):
    import winsound


parser = argparse.ArgumentParser(description='Simple RMI actuator.')
parser.add_argument('name',                   type=str, default='name',           help='The name of the node')
parser.add_argument('host',                   type=str, default='localhost',      help='The host to connect with')
parser.add_argument('ownip', type=str, default='localhost', help='The IP address on which the actuator should host itself')
args = parser.parse_args ()

def IP ():
	return socket.gethostbyname(socket.gethostname())


@Pyro4.expose                               # Expose this class to RMI
@Pyro4.behavior(instance_mode="single")     # Single instance per node
class Actuator:
	# Define methods here to be accessible remotely.
	def shut_down (self):
		os.system ("shutdown -h now")

	def play_sound (self):
		if sys.platform.startswith('win32'):
			winsound.PlaySound('0477.wav', winsound.SND_FILENAME)
		elif sys.platform.startswith('linux'):
			os.system('mpv 0477.wav')
		else:
			os.system ('mplayer 0477.wav')

	# Starts the pyro daemon
	def start (self, name, host, ownip):
		daemon = Pyro4.Daemon (host=ownip)
		uri = daemon.register (Actuator)
		ns = Pyro4.locateNS (host)
		ns.register ('actuator.' + name, uri)

		daemon.requestLoop ()


def main ():
	actuator = Actuator ()
	actuator.start (args.name, args.host, args.ownip)


if __name__ == "__main__":
	main ()
