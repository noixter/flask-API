from flask_restx.errors import abort
from app.users.repositories.sqlalchemy_interface import SQLAlchemyUserRepository
from app.users.services.user_services import UserRestServices, LoginRestServices
from . import api, db
from flask import request
from flask_restx import Resource
from marshmallow import ValidationError
from .serializers import UserSerializer


@api.route('/')
@api.route('/<int:user_id>')
class User(Resource):
    """Users Resource
    methods: GET, POST, PUT, DELETE
    """

    #method_decorators = [jwt_required]
    print_serialize_fields = ['id', 'first_name', 'last_name', 'email', 'rol']
    user_serializer = UserSerializer(only=print_serialize_fields)
    services = UserRestServices(
        user_repository=SQLAlchemyUserRepository(
            db=db
        )
    )

    def get(self, user_id=None):
        if not user_id:
            users = self.services.repository.list()
            result = self.user_serializer.dump(users, many=True)
            return {'count': len(result), 'users': result}, 200

        user = self.services.repository.get(pk=user_id)
        result = self.user_serializer.dump(user)

        return result, 200

    def post(self):
        user_data = request.get_json(force=True)
        self.user_serializer = UserSerializer()
        try:
            user_serialize = self.user_serializer.load(user_data)
            response = self.services.create_object(user_data=user_serialize)
            return response, 201
        except ValidationError as e:
            abort(400, code_error=400, errors=e.messages)

    def put(self, user_id):
        update_fields = request.get_json(force=True)
        try:
            serialize_update_fields = self.user_serializer.load(
                update_fields, partial=True
            )
            self.services.modify_user(
                pk=user_id, update_fields=serialize_update_fields
            )
            return {'code': 200, 'message': 'updated'}, 200
        except ValidationError as e:
            abort(400, code_error=400, errors=e.messages)

    def delete(self, user_id):
        response = self.services.delete_user(pk=user_id)
        return response, response.get('code')


@api.route('/login')
class Login(Resource):
    """Resource for create a token given a specific user throw Login View"""

    user_serializer = UserSerializer(only=['email', 'password'])
    services = LoginRestServices(
        user_repository=SQLAlchemyUserRepository(db=db),
        user_services=UserRestServices(
            user_repository=SQLAlchemyUserRepository(db=db)
        )
    )

    def post(self):
        params = request.get_json(force=True)
        try:
            params_serialize = self.user_serializer.load(params, partial=True)
            response = self.services.login(params=params_serialize)
            return response, 200
        except ValidationError as e:
            abort(400, code_error=400, errors=e.messages)


@api.route('/logout')
class Logout(Resource):
    """Resource for revoked token access throw a LogOut view"""

    #method_decorators = [jwt_required]
    services = LoginRestServices(
        user_repository=SQLAlchemyUserRepository(db=db),
        user_services=UserRestServices(
            user_repository=SQLAlchemyUserRepository(db=db)
        )
    )

    def get(self):
        self.services.logout()


