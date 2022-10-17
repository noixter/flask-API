from typing import List, Optional

import jwt
from flask import request
from flask_restx import Resource
from marshmallow.exceptions import ValidationError

from app.users import api
from app.users.adapters.repository import (SQLAlchemyRoleRepository,
                                           SQLAlchemyUserRepository)
from app.users.serializers import LoginSerializer, UserSerializer
from shared.tools.exceptions import BaseHTTPException
from shared.tools.pyjwt import JWTHandler
from users.constants import TokenTypes
from users.exceptions import NotAuthenticated, ObjectNotFound, PermissionDenied
from users.permissions import AdminUser, BasePermission, IsOwnUser
from users.services.auth import JWTAuth
from users.services.base import AuthServices
from users.services.services import JWTLogin, UserServices, create_tokens


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

        if (
            request.user
            and not any([
                permission.has_permission(request)
                for permission in self.permissions
            ])
        ):
            raise PermissionDenied(
                'user is not allowed to perform this action'
            )

        return super().dispatch_request(*args, **kwargs)


@api.route('/')
@api.route('/<int:user_id>')
class User(BaseResource):

    user_repository = SQLAlchemyUserRepository()
    authentication = [JWTAuth(jwt=JWTHandler())]
    permissions = [AdminUser(), IsOwnUser()]
    print_serialize_fields = ['id', 'first_name', 'last_name', 'email', 'role']
    user_serializer = UserSerializer(only=print_serialize_fields)
    services = UserServices(
        user_repository=user_repository,
        role_repository=SQLAlchemyRoleRepository()
    )

    def get(self, user_id=None):
        if not user_id:
            users = self.services.user_repository.list()
            result = self.user_serializer.dump(users, many=True)
            return {'count': len(result), 'users': result}, 200

        user = self.services.user_repository.get(pk=user_id)
        result = self.user_serializer.dump(user)

        return result, 200

    def post(self):
        user_data = request.get_json(force=True)
        self.user_serializer = UserSerializer()
        user_serialize = self.user_serializer.load(user_data)
        user = self.services.create_user(user_data=user_serialize)
        serialize_user = self.user_serializer.dump(user)
        return serialize_user, 201

    def put(self, user_id):
        update_fields = request.get_json(force=True)
        serialize_update_fields = self.user_serializer.load(
            update_fields, partial=True
        )
        user = self.services.modify_user(
            pk=user_id, update_fields=serialize_update_fields
        )
        serialize_user = self.user_serializer.dump(user)
        return {
            'message': 'updated',
            'user': serialize_user
        }, 200

    def delete(self, user_id):
        # Users cannot delete themselves
        if request.user.id == user_id:  # type: ignore
            raise PermissionDenied('User cannot perform this operation')
        try:
            self.services.delete_user(pk=user_id)
        except ObjectNotFound:
            raise
        return {}, 204


@api.route('/token')
class Token(Resource):

    serializer = LoginSerializer()
    service = JWTLogin(
        repository=SQLAlchemyUserRepository(),
        token_handler=JWTHandler()
    )

    def post(self):
        data = request.get_json(force=True)
        serialize = self.serializer.load(data)
        user_id = serialize.get('user_id')
        password = serialize.get('password')
        response = self.service.login(user_id=user_id, password=password)
        return response, 201


@api.route('/token/refresh')
class RefreshToken(BaseResource):

    jwt = JWTHandler()

    def post(self):
        data = request.get_json(force=True)
        refresh_token = data.get('refresh_token')
        headers = self.jwt.get_token_headers(refresh_token)
        if headers.get('typ') == TokenTypes.ACCESS.name.lower():
            raise NotAuthenticated('Access token not allowed')

        try:
            payload = self.jwt.decode(refresh_token)
            user_id = payload.get('user_id')
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as e:
            raise NotAuthenticated(message=e.args[0])

        response = create_tokens(user_id, self.jwt)
        return response, 201
