import os
import sys
import socket
import Pyro4        # RMI

if sys.platform.startswith('win32'):
    import winsound


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
		else:
			os.system ('mplayer 0477.wav')

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
