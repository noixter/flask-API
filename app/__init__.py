from . import *
from flask import Flask
from .Config import configs
from app.users import ma, api, db as db_users


def create_app(environment):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(environment)
    with app.app_context():
        db_users.init_app(app)
        ma.init_app(app)
        db_users.create_all()
        from app.users import views
    from app.users import users
    app.register_blueprint(users, url_prefix='/users')
    return app

