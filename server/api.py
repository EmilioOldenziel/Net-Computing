import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from . import app, db
from .models import Node

api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('name')

class NodeList(Resource):
    def get(self):
        return jsonify(json_list=[i.serialize for i in Node.query.all()])

    def post(self):
        args = parser.parse_args()
        data = {'name': args['name']}
        new_node = Node(name=data['name'])
        db.session.add(new_node)
        db.session.commit()
        return 'node added', 201

api.add_resource(NodeList, '/api/nodelist/', methods=['POST', 'GET'])