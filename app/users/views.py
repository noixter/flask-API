from typing import Optional, List

import jwt
from marshmallow.exceptions import ValidationError

from app.users.repositories.sqlalchemy_interface import SQLAlchemyUserRepository
from app.users.services.user_services import UserRestServices
from . import api, db
from flask import request
from flask_restx import Resource

from .constants import TokenTypes
from .exceptions import PermissionDenied, NotAuthenticated
from .permissions import BasePermission, AdminUser, IsOwnUser
from .serializers import UserSerializer, TokenSerializer
from .services.auth import JWTAuth
from .services.base_service import AuthServices
from ..tests.tools.exceptions import BaseHTTPException
from ..tools.pyjwt import JWTHandler


@api.errorhandler(BaseHTTPException)
@api.errorhandler(ValidationError)
def render_json_exception(e):
    if not hasattr(e, 'to_dict'):
        if isinstance(e, ValidationError):
            data = dict(errors=e.messages)
            e.data = data
            return data, 400
        return dict(errors=e.args[0]), 400
    return e.to_dict(), e.status_code


class BaseResource(Resource):
    """Extend class to handle authentication and permission classes"""

    authentication: List[Optional[AuthServices]] = []
    permissions: List[Optional[BasePermission]] = []

    def dispatch_request(self, *args, **kwargs):

        for auth in self.authentication:
            if not isinstance(auth, AuthServices):
                raise TypeError(f'{auth} is not {AuthServices} instance')
            try:
                user = auth.validate(request)
                request.user = user
            except ValueError as e:
                raise NotAuthenticated(message=e.args[0])

        for permission in self.permissions:
            if not isinstance(permission, BasePermission):
                raise TypeError(f'{permission} is not a {BasePermission} instance')
            if permission.has_permission(request.user):
                break
            raise PermissionDenied(
                f'user is not allowed to perform this action'
            )

        return super().dispatch_request(*args, **kwargs)


@api.route('/')
@api.route('/<int:user_id>')
class User(BaseResource):
    """Users Resource
    methods: GET, POST, PUT, DELETE
    """

    repository = SQLAlchemyUserRepository(db=db)
    auth = JWTAuth(repository=repository, jwt=JWTHandler())
    authentication = [auth]
    permissions = [AdminUser(), IsOwnUser()]
    print_serialize_fields = ['id', 'first_name', 'last_name', 'email', 'rol']
    user_serializer = UserSerializer(only=print_serialize_fields)
    services = UserRestServices(
        user_repository=repository
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
        user_serialize = self.user_serializer.load(user_data)
        response = self.services.create_object(user_data=user_serialize)
        return response, 201

    def put(self, user_id):
        update_fields = request.get_json(force=True)
        serialize_update_fields = self.user_serializer.load(
            update_fields, partial=True
        )
        self.services.modify_user(
            pk=user_id, update_fields=serialize_update_fields
        )
        return {'code': 200, 'message': 'updated'}, 200

    def delete(self, user_id):
        if request.user.pk == user_id:
            raise PermissionDenied('User cannot perform this operation')
        response = self.services.delete_user(pk=user_id)
        return response, response.get('code')


@api.route('/token')
class Token(Resource):

    serializer = TokenSerializer
    service = UserRestServices
    jwt = JWTHandler

    def post(self):
        data = request.get_json(force=True)
        serialize = self.serializer().load(data, partial=True)
        user_id = serialize.get('user_id')
        response = self.service.create_tokens(user_id, jwt=self.jwt())
        serialize_response = self.serializer().dump(response)
        return serialize_response, 201


@api.route('/token/refresh')
class RefreshToken(BaseResource):

    required_fields = ['refresh_token']
    serializer = TokenSerializer
    service = UserRestServices
    jwt = JWTHandler

    def post(self):
        data = request.get_json(force=True)
        serialize = self.serializer(only=self.required_fields).load(data, partial=True)
        refresh_token = serialize.get('refresh_token')
        headers = self.jwt.get_token_headers(refresh_token)
        if headers.get('typ') == TokenTypes.ACCESS.name.lower():
            raise NotAuthenticated('Not access token allowed')

        try:
            payload = self.jwt().decode(refresh_token)
            user_id = payload.get('user_id')
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as e:
            raise NotAuthenticated(message=e.args[0])

        response = self.service.create_tokens(user_id, self.jwt())
        serialize_response = self.serializer().dump(response)
        return serialize_response, 201
