from typing import Any, Dict, Optional

from flask import Request
from jwt import ExpiredSignatureError, InvalidSignatureError

from app.users.adapters.repository import SQLAlchemyUserRepository
from shared.tools.exceptions import BaseHTTPException
from shared.tools.pyjwt import TokenHandler
from users.constants import TokenTypes
from users.exceptions import NotAuthenticated, ObjectNotFound
from users.models import User
from users.repositories.base_interface import UserRepository
from users.services.base import AuthServices


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
                f'{self.__class__.__name__}: '
                'Either username or password are required'
            )

        user = self.repository.filter_by_email(email=username)
        if not user:
            raise ObjectNotFound(f'User with email: {username} does not exists')

        if not user.password == password:
            raise ObjectNotFound('Password does not correspond')

        return user


class JWTAuth(AuthServices):

    def __init__(
        self,
        jwt: TokenHandler,
        repository: Optional[UserRepository] = None
    ):
        self.repository = repository or SQLAlchemyUserRepository()
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

        try:
            payload = self.jwt.decode(token)
        except (ExpiredSignatureError, InvalidSignatureError):
            raise BaseHTTPException('Token expired or malformed')

        if payload.get('typ') == TokenTypes.REFRESH.name.lower():
            raise NotAuthenticated('Refresh token not allowed')

        user_id = payload.get('user_id')
        user = self.repository.get(pk=int(user_id))
        if not user:
            raise ObjectNotFound('User does not exist')

        return user
