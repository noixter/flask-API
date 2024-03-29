from app import create_app
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from app.Config import configs


enviroment = configs.get('development')
if config('PRODUCTION', default=False):
    enviroment = configs.get('production')


api = create_app(enviroment)
db = SQLAlchemy(api)


@api.route('/', methods=['GET'])
def index():
    return jsonify(message='Welcome, this is a Users API controller',
                   routes_available='/users , /users/login, /users/logout'), 200


if __name__ == '__main__':
    api.run(host='0.0.0.0')