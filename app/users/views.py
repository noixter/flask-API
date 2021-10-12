from . import api
from datetime import datetime, timedelta
from flask import request
from flask_restplus import Resource
from marshmallow import ValidationError
from .models import Users, BlacklistToken
from .serializers import UserSerializer
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)


@api.route('/')
@api.route('/<int:user_id>')
class User(Resource):
    """Users Resource}
    methods: GET, POST, PUT, DELETE
    """

    method_decorators = [jwt_required]
    print_serialize_fields = ['id', 'first_name', 'last_name', 'email', 'rol']
    user_serializer = UserSerializer(only=print_serialize_fields)

    def get(self, user_id=None):

        if not user_id:
            users = Users.query.all()
            result = self.user_serializer.dump(users, many=True)
            return {'count': len(result), 'users': result}, 200

        user = Users.query.filter_by(id=user_id).first()
        result = self.user_serializer.dump(user)

        return result, 200

    def post(self):
        current_user = Users.query.filter_by(
            id=get_jwt_identity()
        ).first()

        if not current_user.rol_id == 1:
            return {'code': 403, 'error': 'Not allowed to create new Users'}, 403

        self.user_serializer = UserSerializer()
        user_data = request.get_json(force=True)

        try:
            user_serialize = Users(**self.user_serializer.load(user_data))
        except ValidationError as e:
            return {'code': 400, 'errors': e.messages}, 400

        if Users.query.get(user_serialize.id):
            return {'code': 400, 'error': 'User with id {} already exist'.
                format(user_serialize.id)}, 400

        user_serialize.create_object()
        return {'code': 201, 'message': 'created'}, 201

    def put(self, user_id):
        current_user = Users.query.filter_by(
            id=get_jwt_identity()
        ).first()
        user_to_update = Users.query.get(user_id)

        if not user_to_update:
            return {'code': 400, 'error': 'User does not exists'}, 400

        if not current_user.rol_id == 1 or not current_user == user_to_update:
            return {'code': 403,
                    'error': 'Not allowed to change this user'
                    }, 403

        update_fields = request.get_json(force=True)

        try:
            serialize_update_fields = self.user_serializer.load(
                update_fields, partial=True
            )
            user_to_update.update_object(serialize_update_fields)
            return {'code': 200, 'message': 'updated'}, 200

        except ValidationError as e:
            return {'code': 400, 'errors': e.messages}, 400

    def delete(self, user_id):
        current_user = Users.query.filter_by(id=get_jwt_identity()).first()
        user_to_delete = Users.query.get(user_id)
        if not user_to_delete:
            return {'code': 400, 'error': 'User does not exists'}, 400

        if current_user.rol_id == 1 or current_user != user_to_delete:
            user_serialize = self.user_serializer.dump(user_to_delete)
            user_to_delete.delete_user()
            return {'code': 200, 'message': 'deleted', 'user': user_serialize}, 200


@api.route('/login')
class Login(Resource):
    """Resource for create a token given a specific user throw Login View"""

    user_serializer = UserSerializer(only=['email', 'password'])

    def post(self):
        user = request.get_json(force=True)
        if not user:
            return {'code': 400, 'error': 'No username or password to authenticate'}, 400

        try:
            user_serialize = self.user_serializer.load(user, partial=True)
        except ValidationError as e:
            return {'code': 400, 'errors': e.messages}, 400

        user_to_login = Users.query.filter_by(email=user_serialize.get('email')).first()

        if not user_to_login:
            return {'code': 400, 'error': 'username does not exist'}, 400

        if not user_to_login.password == user.get('password'):
            return {'code': 401, 'error': 'Username or password incorrect'}, 401

        access_token = create_access_token(identity=user_to_login.id)
        expires = datetime.timestamp(datetime.now() + timedelta(days=1))

        return {'user': user_to_login.email, 'access_token': access_token, 'expires': expires}, 200


@api.route('/logout')
class Logout(Resource):
    """Resource for revoked token access throw a LogOut view"""

    method_decorators = [jwt_required]

    def get(self):
        current_user = Users.query.filter_by(id=get_jwt_identity()).first()
        access_token = get_raw_jwt()
        token_blacklisted = {
            'token': access_token['jti'],
            'expires': BlacklistToken().transform_expires_to_date(access_token['exp']),
            'user_id': access_token['identity']
        }
        token = BlacklistToken(**token_blacklisted)
        token.add()
        return {'code': 200, 'message': 'Successfully logout user {}'.format(current_user.email)}, 200


