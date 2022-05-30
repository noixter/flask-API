from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy.exc import IntegrityError

from app.tools.pyjwt import JWTHandler
from app.users.constants import TokenTypes
from app.users.repositories.base_interface import UserRepository

from flask_restx import abort


class UserRestServices:

    def __init__(
        self,
        user_repository: UserRepository
    ):
        self.repository = user_repository

    def create_object(self, user_data: dict) -> dict:
        if self.repository.filter_by_email(email=user_data.get('email')):
            abort(
                400, code_error=400,
                error=f'User with email {user_data.get("email")} already exist'
            )

        self.repository.add(user_data)
        return {'code': 201, 'message': 'created'}

    def modify_user(self, pk: int, update_fields: dict) -> Dict[str, Any]:
        user_to_update = self.repository.get(pk=pk)
        if not user_to_update:
            abort(400, code_error=400, error='User does not exists')

        user = self.repository.modify(
            pk=user_to_update.id, update_fields=update_fields
        )
        if not user:
            abort(400, code_error=400, errors='user not found')
        return {'code': 200, 'message': 'updated'}

    def delete_user(self, pk: int) -> Optional[Dict[str, Any]]:
        try:
            self.repository.delete(pk=pk)
            return {'code': 200, 'message': 'deleted'}
        except IntegrityError:
            abort(400, code_error=400, error='User does not exists')

    @classmethod
    def create_tokens(cls, user_id: int, jwt: JWTHandler) -> Dict[str, Any]:
        response = dict(user_id=user_id)
        for type_ in TokenTypes:
            expiration = type_.value.get('expiration')
            expires_at = datetime.now() + timedelta(hours=expiration)
            token = jwt.encode(
                user_id=user_id, type_=type_.name.lower(),
                expires_at=expires_at
            )
            response[f'{type_.name.lower()}_token'] = token

        return response
