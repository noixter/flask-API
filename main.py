from app import create_app
from flask import jsonify
from decouple import config
from app.Config import configs


environment = configs.get('development')
if config('PRODUCTION', default=False):
    environment = configs.get('production')

api = create_app(environment)


@api.route('/', methods=['GET'])
def index():
    return jsonify(message='Welcome, this is a Users API',
                   routes_availables='/users , /users/login, /users/logout'), 200


if __name__ == '__main__':
    api.run(host='0.0.0.0', debug=True)
