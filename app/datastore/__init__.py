from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

datastore = Blueprint('data', __name__, url_prefix='/data')
db = SQLAlchemy()

from . import views