import requests
import json
from app import create_app
from app.users.models import Users
from flask import render_template, request, url_for, jsonify, redirect
from flask_login import current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from app.Config import configs


enviroment = configs.get('development')
if config('PRODUCTION', default=False):
    enviroment = configs.get('production')

api = create_app(enviroment)
db = SQLAlchemy(api)


@api.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        import ipdb; ipdb.set_trace()
        response = requests.post('http://localhost:5000/users/login', data=json.dumps(data))
        print(response)
        user_to_login = Users.query.filter_by(email=data.get('email')).first()
        if user_to_login:
            if user_to_login.password == data.get('password'):
                login_user(user_to_login)
                return redirect('http://google.com')
            else:
                return 'Password not valid'
        else:
            return 'User does not exist'

    else:
        if current_user.is_authenticated:
            print('Ya loggeado')
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


@api.route('/index', methods=['GET'])
@login_required
def index():
    return 'Bienvenido {}'.format(current_user)


if __name__ == '__main__':
    api.run(host='0.0.0.0')