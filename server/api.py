import json
import platform
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort

from . import app, db
from .models import Node, Sensor, Measurement

api = Api(app)

class NodeList(Resource):
    def get(self):
        return jsonify(json_list=[i.serialize for i in Node.query.all()])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('ip')
        args = parser.parse_args()
        data = {'name': args['name'], 'ip': args['ip']}
        """ if name already exits """
        if(Node.query.filter_by(name=data['name']).count() > 0):
            response = jsonify(node_id=None)
            response.status_code = 403
            return response
        """ add node and return setup for mq """
        new_node = Node(name=data['name'], ip=data['ip'])
        db.session.add(new_node)
        db.session.commit()
        response =  jsonify(node_id=new_node.id,
                            # q_host='localhost',
                            q_host='145.97.145.188',
                            q_name='mq')
        response.status_code = 201
        return response

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        data = {'id': args['id']}
        node = Node.query.get(data['id'])
        db.session.delete(node)
        db.session.commit()
        return 'node added', 201        

api.add_resource(NodeList, '/api/nodelist/', methods=['POST', 'GET', 'DELETE'])

class SensorList(Resource):
    def get(self):
        return jsonify(json_list=[i.serialize for i in Sensor.query.all()])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        data = {'name': args['name']}
        new_node = Sensor(name=data['name'])
        db.session.add(new_node)
        db.session.commit()
        return 'Sensor added', 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        data = {'id': args['id']}
        sensor = Sensor.query.get(data['id'])
        db.session.delete(sensor)
        db.session.commit()
        return 'Sensor deleted', 201 

api.add_resource(SensorList, '/api/sensorlist/', 
    methods=['POST', 'GET', 'DELETE'])


class MeasurementList(Resource):
    def get(self):
        return jsonify(json_list=[i.serialize for i in Measurement.query.all()])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('value_type')
        parser.add_argument('unit')
        parser.add_argument('value')
        args = parser.parse_args()
        measurement = Measurement(**args)
        db.session.add(measurement)
        db.session.commit()
        return 'Measurement added', 201

api.add_resource(MeasurementList, '/api/measurementslist/', 
    methods=['POST', 'GET'])
