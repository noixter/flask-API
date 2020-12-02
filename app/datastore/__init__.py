from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from kombu import Connection
from dotenv import load_dotenv
import os

load_dotenv()

datastore = Blueprint('data', __name__, url_prefix='/data')
db = SQLAlchemy()
#client = MongoClient('localhost', 27017)
broker = Connection('pyamqp://{}:{}@{}:{}//'.format(str(os.getenv('BROKER_USER')), str(os.getenv('BROKER_PASS')),
                                                    str(os.getenv('BROKER_URL')), str(os.getenv('BROKER_PORT'))))


from . import views
