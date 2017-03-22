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
        parser.add_argument('ip')
        args = parser.parse_args()
        data = {'name': args['name'], 'ip': args['ip']} 
        new_node = Node(name=data['name'], ip=data['ip'])
        db.session.add(new_node)
        db.session.commit()
        return new_node.id, 201

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
