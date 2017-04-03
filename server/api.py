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
        args = parser.parse_args()

        try:
           node = Node.query.filter_by(name=args['name']).one()
           node.ip = request.remote_addr
        except:
            # Add node
            node = Node(
                name=args['name'], 
                ip=request.remote_addr
            )
            db.session.add(node)
        
        db.session.commit()

        # return setup for mq
        response =  jsonify(
            node_id=node.id,
            q_host=app.config.get('MQ_HOST', ''),
            q_name=app.config.get('MQ_NAME', '')
        )
        response.status_code = 201
        return response

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        node = Node.query.get(args['id'])
        db.session.delete(node)
        db.session.commit()
        return 'Node deleted', 200

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
        return 'Sensor deleted', 200

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
