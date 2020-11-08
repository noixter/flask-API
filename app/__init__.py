from flask import Flask
from .Config import Config
from app.users import users, db
from app.datastore import datastore, db as datastore_db
from app.users.models import Users, Role
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


login_manager = LoginManager()
login_manager.login_view = 'users.login'

db = SQLAlchemy()
jwt = JWTManager()


@login_manager.user_loader
def load_user(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    return user


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        datastore_db.init_app(app)
        datastore_db.create_all()
    login_manager.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(users)
    app.register_blueprint(datastore)
    return app

