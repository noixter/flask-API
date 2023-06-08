from flask import Blueprint
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

users = Blueprint("users", __name__, url_prefix="/users")
api = Api(users)
db = SQLAlchemy()
ma = Marshmallow()

from . import views  # noqa
