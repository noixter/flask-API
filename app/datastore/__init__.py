from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from kombu import Connection
from decouple import config
import os

datastore = Blueprint('data', __name__, url_prefix='/data')
db = SQLAlchemy()
# client = MongoClient('localhost', 27017)
broker = Connection('pyamqp://{}:{}@{}//'.format(config('USER_BROKER', default='guest'),
                                                 config('PASSWD_BROKER', default='guest'),
                                                 config('URL_BROKER', default='localhost:5672')))

from . import views
