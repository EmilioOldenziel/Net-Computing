from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime

# Init app
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api, views, models