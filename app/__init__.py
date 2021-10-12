from . import *
from flask import Flask
from .Config import configs
from app.users import users, ma, db as users_db
from app.users.models import BlacklistToken
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()


# Function callback to evaluate if a token has been revoked
@jwt.token_in_blacklist_loader
def check_blacklisted_token(token):
    blacklisted_token = BlacklistToken.query.filter_by(token=token.get('jti')).first()
    if blacklisted_token:
        return True
    else:
        return False


def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    with app.app_context():
        users_db.init_app(app)
        ma.init_app(app)
        users_db.create_all()
    jwt.init_app(app)
    app.register_blueprint(users)
    return app

