from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

datastore = Blueprint('data', __name__, url_prefix='/data')
db = SQLAlchemy()
client = MongoClient('localhost', 27017)


from . import views