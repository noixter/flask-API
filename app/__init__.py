from flask import Flask

from app.users import db as db_users
from app.users import ma

from . import *  # noqa
from .config import configs


def create_app(env):
    app = Flask(__name__)
    environment = configs.get(env)
    app.config.from_object(environment)
    with app.app_context():
        db_users.init_app(app)
        ma.init_app(app)
        from app.users import commands, views
        db_users.create_all(app=app)

    from app.users import users
    app.register_blueprint(users, url_prefix='/users')

    return app
