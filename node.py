#!/usr/bin/env python

import argparse
import json
import pika
import platform
import pprint
import random
import requests
import sys

import subprocess   # Starting a process

if sys.platform.startswith("linux"):
    import sensors
elif sys.platform.startswith('win32'):
    import wmi
    sensors = wmi.WMI(namespace='root\OpenHardwareMonitor')

from time import sleep
from datetime import datetime as dt


parser = argparse.ArgumentParser(description='Read sensor data')
parser.add_argument('name',                   type=str,                                                  help='The name of the node')
parser.add_argument('host',                   type=str, nargs="?", default='http://localhost:5000',      help='The host to connect with')
parser.add_argument('-s', '--sensor',         type=str, default='system',                                help='The TXT email source file. (default: mail.txt)')
args = parser.parse_args()

class LinuxDataCollector:
    """ gets hardware sensor measurements for linux systems """
    measurement_units = {
        2: 'celsius'
    }
    
    def get_measurements(self):
        def generate(data):
            for chip in data:
                for feature in chip:
                    print(feature)
                    if feature.type in self.measurement_units:
                        yield {
                            'label': feature.label,
                            'value': feature.get_value(),
                            'unit': self.measurement_units[feature.type]
                        }

        sensors.init()
        
        try:
            measurements = list(generate(sensors.iter_detected_chips()))
        finally:
            sensors.cleanup()

        return measurements


class WindowsDataCollector:
    """ 
    gets hardware sensor measurements for windows systems 
    (requires OpenHardwareMonitor)
    """

    measurement_units = {
        'Temperature': 'celsius',
        # 'Load': 'percent',
        # 'Fan': 'rpm',
    }

    def get_measurements(self):
        def generate(sensors):
            for sensor in sensors:
                if sensor.SensorType in self.measurement_units:
                    yield {
                        'label': sensor.Name,
                        'value': sensor.Value,
                        'unit': self.measurement_units[sensor.SensorType],
                    }

        return list(generate(sensors.Sensor()))

class MacOSDataCollector:
    # TODO: This needs to be expanded.
    def get_measurements(self):
        return [3, 4]


class RandomDataCollector:
    """ simulates hardware sensor measurements """
    def __init__(self):
        self.cores = 2 ** random.randrange(4)
        self.data = dict( ('core {}'.format(c), 
            random.random() * 80 + 20) for c in range(self.cores) )

    def get_measurements(self):
        def generate():
            for core in self.data:
                self.data[core] += random.random() * 4 - 2
                self.data[core] = min(150, max(10, self.data[core]))
                yield {
                    'label': core,
                    'value': self.data[core],
                    'unit': 'celsius',
                }
        return list(generate())


def _get_datacollector():
    if args.sensor == 'random':
        return RandomDataCollector()
        
    elif args.sensor == 'system':
        if sys.platform.startswith("linux"):
            return LinuxDataCollector()
        elif sys.platform.startswith('win32'):
            return WindowsDataCollector()
        elif sys.platform.startswith('darwin'):
            return MacOSDataCollector()
        raise Exception("Unsupported platform")

    raise Exception("Invalid sensor")


class Node:
    def __init__(self, given_host, queue_name, node_id):
        self.node_id = node_id
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=given_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

        self.datacollector = _get_datacollector()

    def measure(self):
        return self.datacollector.get_measurements()
        
    def run(self):
        while True:
            message = {
                'id': self.node_id,
                'ts': str(dt.now()),
                'measurements': self.measure()
            }

            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message)
            )

            print(' [x] Sent measurement by {}'.format(message['id']))
            
            sleep(1)

        self.connection.close()


def get_ip_address():
    """
        TODO: implement ip return
    """
    return "my_awesome_ip"

def setup_node(name, host):
    # Start actuator
    subprocess.Popen (["python", "actuator.py"])

    node_ip = get_ip_address()
    host = host + '/api/nodelist/'
    data = {
        'name': name,
        'ip': node_ip
    }
    r = requests.post(host, data)
    print(r.text)
    sd = json.loads(r.text)
    
    if r.status_code == 201:
        return Node(sd['q_host'], sd['q_name'], sd['node_id'])
    if r.status_code == 403 and sd['node_id'] == None:
        exit("name already in use")


if __name__ == "__main__":
    node = setup_node(args.name, args.host)
    node.run()
