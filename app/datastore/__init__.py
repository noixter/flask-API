from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from celery import Celery
import os

datastore = Blueprint('data', __name__, url_prefix='/data')
db = SQLAlchemy()
client = MongoClient('localhost', 27017)
broker = Celery('publisher', broker='amqp://{}:{}@{}/'.format(os.environ.get('USER_BROKER'),
                                                              os.environ.get('PASSWD_BROKER'),
                                                              os.environ.get('URL_BROKER')))

from . import views
