from datetime import datetime
from . import db
import json

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
           'created at': str(self.created),
        }


class Sensor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), unique=True)
    node_id = db.Column(db.Integer(), db.ForeignKey('node.id'))
    updated = db.Column(db.DateTime())
    created = db.Column(db.DateTime())
    node = db.relationship('Node', backref='sensors')

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


class Measurement(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    node_id = db.Column(db.Integer(), db.ForeignKey('node.id'))
    value_type = db.Column(db.String(10), nullable=False)
    unit = db.Column(db.String(3), nullable=False)
    value = db.Column(db.Float(), nullable=False)
    timestamp = db.Column(db.DateTime())
    node = db.relationship('Node', backref='measurements')
