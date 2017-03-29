import platform
import Pyro4        # RMI

@Pyro4.expose                               # Expose this class to RMI
@Pyro4.behavior(instance_mode="single")     # Single instance per node
class Actuator:
	# Define methods here to be accessible remotely.

	# Starts the pyro daemon
	def start (self):
		Pyro4.Daemon.serveSimple(
			{
				Actuator: "actuator"
			},
			host = platform.node (),
			ns = False
			)

def main ():
	actuator = Actuator ()
	actuator.start ()

if __name__ == "__main__":
	main ()
