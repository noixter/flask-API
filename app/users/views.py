from . import users, api
from datetime import datetime, timedelta
from flask import request, jsonify
from flask_restplus import Resource
from marshmallow import ValidationError
from .models import Users
from .serializers import UserSerializer, UserPostSerializer
from flask_login import login_user, current_user, login_required, logout_user
from flask_jwt_extended import create_access_token


@api.route('/get_user')
@api.route('/get_user/<int:user_id>')
class User(Resource):
    method_decorators = [login_required]
    user_serializer = UserSerializer()

    def get(self, user_id=None):
        if user_id:
            user = Users.query.filter_by(id=user_id).first()
            result = self.user_serializer.dump(user)
            return result, 200
        else:
            users = Users.query.all()
            result = self.user_serializer.dump(users, many=True)
            return {'count': len(result), 'users': result}, 200

    def post(self):
        if current_user.rol_id == 1:
            self.user_serializer = UserPostSerializer()
            user_data = request.get_json(force=True)
            try:
                user_serialize = Users(**self.user_serializer.load(user_data))
            except ValidationError as e:
                return e.messages, 400
            user_serialize.create_object()
            return {'message': 'created'}, 201
        else:
            return {'error': 'Not allowed to create new Users'}, 403

    def put(self, user_id):
        user_to_update = Users.query.get(user_id)
        update_fields = request.get_json(force=True)
        try:
            serialize_update_fields = self.user_serializer.load(update_fields, partial=True)
            user_to_update.update_object(serialize_update_fields)
            return {'message': 'updated'}, 200
        except ValidationError as e:
            return e.messages, 400

    def delete(self, user_id):
        user_to_delete = Users.query.filter_by(id=user_id).first()
        if not user_to_delete:
            return {'error': 'User does not exists'}, 400
        user_serialize = self.user_serializer.dump(user_to_delete)
        user_to_delete.delete_user()
        return {'message': 'deleted', 'user': user_serialize}, 200





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


@users.route('/serializer', methods=['GET'])
def user_serializer():
    users_serializer = UserSerializer()
    users = Users.query.all()
    result = users_serializer.dump(users, many=True)
    return jsonify(count=len(result), users=result), 200


@users.errorhandler(404)
def not_found(e):
    print(type(e))
    return jsonify(error='We have not fount what you looking for'), 404
