import Pyro4

test_object = Pyro4.Proxy("PYRO:actuator@RN-145-97-135-165.eduroam.rug.nl:57557")
test_object.shut_down ()

