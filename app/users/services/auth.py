from typing import Optional, Any, Dict
from flask import Request
from jwt import ExpiredSignatureError, InvalidSignatureError

from app.tests.tools.exceptions import BaseHTTPException
from app.tools.pyjwt import JWTHandler
from app.users.constants import TokenTypes
from app.users.exceptions import ObjectNotFound, NotAuthenticated
from app.users.models import User
from app.users.repositories.base_interface import UserRepository
from app.users.services.base_service import AuthServices


class BasicAuth(AuthServices):

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def validate(
        self,
        request: Optional[Request] = None,
        **kwargs: Dict[str, Any]
    ) -> User:
        username = request.authorization.username
        password = request.authorization.password
        if not username or not password:
            raise BaseHTTPException(
                f'{self.__class__.__name__}: Either username or password are required'
            )

        user = self.repository.filter_by_email(email=username)
        if not user:
            raise ObjectNotFound(f'User with email: {username} does not exists')

        if not user.password == password:
            raise ObjectNotFound(f'Password does not correspond')

        return user


class JWTAuth(AuthServices):

    def __init__(self, repository: UserRepository, jwt: JWTHandler):
        self.repository = repository
        self.jwt = jwt

    def validate(
        self,
        request: Optional[Request] = None,
        **kwargs: Dict[str, Any]
    ):
        authorization = request.headers.get('Authorization')
        if not authorization:
            raise NotAuthenticated('Token not found')
        token = authorization.rsplit(' ')[1]
        headers = self.jwt.get_token_headers(token)
        if headers.get('typ') == TokenTypes.REFRESH.name.lower():
            raise NotAuthenticated('Not refresh token allowed')

        try:
            payload = self.jwt.decode(token)
        except (ExpiredSignatureError, InvalidSignatureError):
            raise BaseHTTPException(f'Token expired or malformed')

        user_id = payload.get('user_id')
        user = self.repository.get(pk=user_id)
        if not user:
            raise ObjectNotFound(f'User does not exist')

        return user










