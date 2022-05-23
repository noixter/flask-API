from typing import Optional
from flask import Request
from jwt import ExpiredSignatureError, InvalidSignatureError

from app.tools.pyjwt import JWTHandler
from app.users.exceptions import ObjectNotFound
from app.users.models import User
from app.users.repositories.base_interface import UserRepository
from app.users.services.base_service import AuthServices


class BasicAuth(AuthServices):

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def validate(self, request: Optional[Request] = None) -> User:
        username = request.authorization.username
        password = request.authorization.password
        if not username or password:
            raise ValueError(f'{self.__name__}: Either username or password are required')

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

    def validate(self, request: Optional[Request] = None):
        token = request.headers.get('Authorization').rsplit(' ', 1)[0]
        if not token:
            raise ValueError('Token not found')

        try:
            payload = self.jwt.decode(token)
        except (ExpiredSignatureError, InvalidSignatureError) as e:
            raise f'error on token: {e}'

        user_id = payload.get('user_id')
        user = self.repository.get(pk=user_id)
        if not user:
            raise ObjectNotFound(f'User does not exist')

        return User










