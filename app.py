"""
This is configuration file of the application.

In this file logging is set up, setting up route to the database, initializing Flask,
SQLAlchemy and Marshmallow.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database
from flask_migrate import Migrate
import logging
from dotenv import dotenv_values

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('logging.txt')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

env_values = dotenv_values()
USER = env_values.get('USER')
USER_PASS = env_values.get('PASSWORD')
DATABASE_NAME = env_values.get('DB_NAME')
DATABASE_URL = f'mysql+pymysql://{USER}:{USER_PASS}@localhost/{DATABASE_NAME}'

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sfdf782943helwgDR678DVFDHTIWJ3K'
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
from rest.restapi import api

app.register_blueprint(api, url_prefix='/api')

from models.university import University
from models.teacher import Teacher

migrate.init_app(app, db)

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
    db.create_all()
    from database.populate_db import populate_database
    populate_database()

db.create_all()
from views import teacher_view
