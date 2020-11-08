from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

users = Blueprint('users', __name__, url_prefix='/users')
db = SQLAlchemy()

from . import views
