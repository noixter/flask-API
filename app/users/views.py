from . import users
from datetime import datetime, timedelta
from flask import request, jsonify, session
from .models import Users
from flask_login import login_user, current_user, login_required, logout_user
from flask_jwt_extended import create_access_token


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return jsonify(alert="Already login user", user=current_user.email)
        user = request.get_json()
        if not user:
            user = request.form
        email = user['email']
        password = user['password']
        user_to_login = Users.query.filter_by(email=email).first()
        if user_to_login:
            if user_to_login.password == password:
                login_user(user_to_login)
                access_token = create_access_token(identity=user_to_login.user_id)
                expires = datetime.timestamp(datetime.now() + timedelta(days=1))
                return jsonify(user=user_to_login.email, access_token=access_token, expires=expires), 200
            else:
                return jsonify(error='Username or password incorrect'), 401
        else:
            return jsonify(error='username does not exist'), 404
    else:
        return jsonify(message='Please log in with a valid user'), 405


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "User logout"}), 200


@users.route('/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@users.route('/', methods=['GET', 'POST'])
@login_required
def get_user(user_id=None):
    """User endpoint, actions available:
        get a list of user, get a simple user, update a user
        delete user.
        :params user_id if not provided a list of all users will be returned
                if provided actions can be applied to a specific user
    """
    if user_id:
        return Users.get_delete_put_post(item_id=user_id)
    else:
        users = Users.get_delete_put_post(item_id=user_id)
        if request.method == 'POST':
            if current_user.rol_id == 1:
                return jsonify(message='created', user=users.json), 201
            else:
                return jsonify(error='Not allowed to created users'), 401
        else:
            return jsonify(count=len(users.json), users=users.json), 200


@users.errorhandler(404)
def not_found(e):
    print(type(e))
    return jsonify(error='We have not fount what you looking for'), 404
