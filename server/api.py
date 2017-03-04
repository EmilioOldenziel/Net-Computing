import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from . import app, db
from .models import Node, Sensor

api = Api(app)

class NodeList(Resource):
    def get(self):
        return jsonify(json_list=[i.serialize for i in Node.query.all()])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        data = {'name': args['name']}
        new_node = Node(name=data['name'])
        db.session.add(new_node)
        db.session.commit()
        return 'node added', 201

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

# class MeasurementList(Resource):
#     def get(self):
#         return jsonify(json_list=[i.serialize for i in Sensor.query.all()])

#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('sensor'), 
#         parser.add_argument('value_type')
#         parser.add_argument('unit')
#         parser.add_argument('value')
#         args = parser.parse_args()
#         print(args)
#         data = {
#             'sensor': args['sensor'],
#             'value_type': args['value_type'],
#             'unit': args['unit'],
#             'value': args['value']
#         }
#         sensor = Sensor.query.get(data['sensor'])
#         new_measurement = Sensor(
#             sensor=sensor,
#             value_type=data['value_type'],
#             unit=data['unit'],
#             value=data['value'])
#         db.session.add(new_measurement)
#         db.session.commit()
#         return 'Measurement added', 201

#     # def delete(self):
#     #     parser = reqparse.RequestParser()
#     #     parser.add_argument('id')
#     #     args = parser.parse_args()
#     #     data = {'id': args['id']}
#     #     sensor = Sensor.query.get(data['id'])
#     #     db.session.delete(sensor)
#     #     db.session.commit()
#     #     return 'Sensor deleted', 201 
# api.add_resource(MeasurementList, '/api/measurementlist/', 
#     methods=['POST', 'GET', 'DELETE'])
