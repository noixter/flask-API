from flask import Blueprint
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

users = Blueprint('users', __name__)
api = Api(
    users,
    title='Users Api',
    version='0.0.1',
    description='A simple users api'
)
db = SQLAlchemy()
ma = Marshmallow()
