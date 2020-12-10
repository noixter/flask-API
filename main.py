from app import create_app
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from app.Config import configs

enviroment = configs.get('development')
if config('PRODUCTION', default=False):
    enviroment = configs.get('production')

api = create_app(enviroment)
db = SQLAlchemy(api)


@api.route('/')
@login_required
def index():
    return 'Simple API of: {} {}'.format(current_user.first_name, current_user.last_name)


if __name__ == '__main__':
    api.run(host='0.0.0.0')