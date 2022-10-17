from decouple import config
from flask import jsonify

from app import create_app

env = config('ENVIRONMENT', default='development')
api = create_app(env)


@api.route('/', methods=['GET'])
def index():
    return jsonify(message='Welcome, this is a Users API',
                   routes_availables='/users , /users/login, /users/logout'), 200


if __name__ == '__main__':
    api.run(host='0.0.0.0', debug=True)
