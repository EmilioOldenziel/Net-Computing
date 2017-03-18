#!/usr/bin/env python

import pika, random, sensors, json
from time import sleep

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='Nodes')

    node_nr = unicode(random.randint(1, 100))
    message = {}
    message['name']= "nodename" + node_nr
    
    while(1):
        message['measurements'] = measure()
        json_message = json.dumps(message)
        channel.basic_publish(exchange='',
                        routing_key='Nodes',
                        body=json_message)

        print(" [x] Sent measurement by" + message['name'])
        sleep(1)
    connection.close()

""" gets hardware sensor measurements """
def measure():
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

main()