from datetime import datetime, timedelta
from typing import Any, Dict

from app.users.adapters.repository import SQLAlchemyUserRepository
from shared.tools.pyjwt import JWTHandler, Token, TokenHandler
from users.constants import TokenTypes
from users.exceptions import NotAuthenticated, ObjectNotFound, ValidationError
from users.models import User
from users.repositories.base_interface import RoleRepository, UserRepository
from users.services.base import LoginServices


def create_tokens(user_id: int, handler: TokenHandler) -> Dict[str, Any]:
    response = dict()
    for type_ in TokenTypes:
        expiration = type_.value.get('expiration')
        expires_at = datetime.now() + timedelta(hours=expiration)
        token = handler.encode(
            user_id=user_id, type_=type_.name.lower(),
            expires_at=expires_at
        )
        response[f'{type_.name.lower()}_token'] = token

    return response


class JWTLogin(LoginServices):

    def __init__(
        self, repository: UserRepository,
        token_handler: TokenHandler
    ):
        self.repository = repository or SQLAlchemyUserRepository()
        self.token_handler = token_handler or JWTHandler()

    def login(self, user_id: int, **kwargs) -> Dict[str, Token]:
        password = kwargs.get('password')
        user = self.repository.get(pk=user_id)
        if not user:
            raise ObjectNotFound('user does not exists')
        if user.password != password:
            raise NotAuthenticated('incorrect credentials')
        tokens = create_tokens(user_id=user_id, handler=self.token_handler)
        return tokens


class UserServices:

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def create_user(self, user_data: dict) -> User:
        if self.user_repository.filter_by_email(email=user_data.get('email')):
            raise ValidationError(
                f'User with email {user_data.get("email")} already exist'
            )
        role = self.role_repository.get(user_data.get('role_id'))
        if not role:
            raise ValidationError(
                f'role with id {user_data.get("role_id")} does not exists'
            )
        user = self.user_repository.add(user_data)
        return user

    def modify_user(self, pk: int, update_fields: dict) -> User:
        user = self.user_repository.modify(
            pk=pk, update_fields=update_fields
        )
        if not user:
            raise ValidationError('User does not exists')
        return user

    def delete_user(self, pk: int) -> None:
        try:
            self.user_repository.delete(pk=pk)
        except ObjectNotFound as e:
            raise e
