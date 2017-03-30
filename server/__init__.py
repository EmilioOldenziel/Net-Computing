from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_sockets import Sockets

from geventwebsocket import Resource

from datetime import datetime

# Init app
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# sockets = Sockets(app)

from . import api, views, models

from .sockets import MeasurementsApplication

resources = Resource(apps=[
    ('^/measurements', MeasurementsApplication),
    ('^/.*', app)
])
