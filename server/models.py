from datetime import datetime
from . import db
import json

class Sensor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), unique=True)
    node = db.Column(db.Integer(), db.ForeignKey('node.id'))
    updated = db.Column(db.DateTime())
    created = db.Column(db.DateTime())

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name' : self.name,
           'created at': json.dumps(self.created.isoformat()),
        }

    def __init__(self, **kwargs):
        now =  datetime.now()
        self.created = now
        self.updated = now
        super(Sensor, self).__init__(**kwargs)

class Node(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), unique=True)
    ip = db.Column(db.String(30), unique=False)
    updated = db.Column(db.DateTime())
    created = db.Column(db.DateTime())
    

    def __init__(self, **kwargs):
        now =  datetime.now()
        self.created = now
        self.updated = now
        super(Node, self).__init__(**kwargs)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name' : self.name,
           'ip' : self.ip,
           'created at': json.dumps(self.created.isoformat()),
        }

class Measurement(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sensor = db.Column(db.Integer(), db.ForeignKey('sensor.id'))
    value_type = db.Column(db.String(10), nullable=False)
    unit = db.Column(db.String(3), nullable=False)
    value = db.Column(db.Float(), nullable=False)
