#!/usr/bin/env python

import pika, random, sensors, json, requests, sys
from time import sleep

def start_connection(host, queue_name, node_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    message = {}
    message['id']=  node_id
    
    while(1):
        message['measurements'] = measure_linux()
        json_message = json.dumps(message)
        channel.basic_publish(exchange='',
                        routing_key=queue_name,
                        body=json_message)

        print(" [x] Sent measurement by" + message['id'])
        sleep(1)
    connection.close()

""" gets hardware sensor measurements """
def measure_linux():
    sensors.init()
    measurements_list = []

    measurements_unit = {
        2: 'celsius'
    }

    try:
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                print(feature)
                measurements_list.append(
                    {
                        'label': feature.label,
                        'value': feature.get_value(),
                        'unit': measurements_unit[feature.type]
                    }
                )
    finally:
        sensors.cleanup()
    
    return measurements_list

def setup_node(name, host):
    node_ip = "ipswag"
    host = host + '/api/nodelist/'
    data = {
        'name': name,
        'ip': node_ip
    }
    r = requests.post(host, data)
    node_id = r.text

    start_connection('localhost', "mq", node_id)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('We need 2 arguments: name, host')
    name = sys.argv[1]
    host = sys.argv[2]
    setup_node(name, host)