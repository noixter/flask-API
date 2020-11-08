from . import users
from flask import request, jsonify, redirect, url_for
from .models import Users
from flask_login import login_user, current_user
from flask_jwt_extended import create_access_token


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('users.index'))
        user = request.get_json()
        email = user['email']
        password = user['password']
        user_to_login = Users.query.filter_by(email=email).first()
        if user_to_login:
            if user_to_login.password == password:
                login_user(user_to_login)
                access_token = create_access_token(identity=user_to_login.user_id)
                return jsonify(user=user_to_login.email, access_token=access_token), 200
            else:
                return jsonify(error='Username or password incorrect'), 403
        else:
            return jsonify(error='username does not exist'), 403
    else:
        return jsonify(message='Please log in with a valid user')


@users.route('/get_user/<email>', endpoint='get_user', methods=['GET'])
def users(email):
    return Users.get_delete_put_post(prop_filters={'email': email})
