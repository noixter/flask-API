from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy.exc import IntegrityError

from app.users.services.base_service import UserServices, LoginServices
from app.users.repositories.base_interface import UserRepository

from flask_restx import abort


class UserRestServices(UserServices):

    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository
        self.current_user = self.repository.get(
            pk=1
        )

    def create_object(self, user_data: dict) -> dict:
        if not self.current_user.rol_id == 1:
            abort(403, code_error=403, error='Not allowed to create new Users')

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

        if (
            not self.current_user.rol_id == 1
            and not self.current_user == user_to_update
        ):
            abort(403, code_error=403, error='Not allowed to change this user')

        user = self.repository.modify(
            pk=user_to_update.id, update_fields=update_fields
        )
        if not user:
            abort(400, code_error=400, errors='user not found')
        return {'code': 200, 'message': 'updated'}

    def delete_user(self, pk: int) -> Optional[Dict[str, Any]]:
        if self.current_user.rol_id == 1 or self.current_user.id != pk:
            try:
                self.repository.delete(pk=pk)
                return {'code': 200, 'message': 'deleted'}
            except IntegrityError:
                abort(400, code_error=400, error='User does not exists')

    def create_access_token(self, pk: int):
        user = self.repository.get(pk=pk)
        if user:
            #access_token = create_access_token(identity=user.id)
            expires = datetime.timestamp(datetime.now() + timedelta(days=1))
            #return {'access_token': access_token, 'expires': expires}
        return {'error': 'user does not exists'}


class LoginRestServices(LoginServices):

    def __init__(
        self, user_repository: UserRepository,
        user_services: UserServices
    ):
        self.repository = user_repository
        self.services = user_services

    def login(self, params: dict) -> dict:
        if not params:
            abort(400, code_error=400, error='No username or password to authenticate')

        user_to_login = self.repository.filter_by_email(email=params.get('email'))

        if not user_to_login:
            abort(400, code_error=400, error='username does not exist')

        if not user_to_login.password == params.get('password'):
            abort(401, code_error=401, error='Username or password incorrect')

        access_token = self.services.create_access_token(user_id=user_to_login.id)
        expires = datetime.timestamp(datetime.now() + timedelta(days=1))

        return {'user': user_to_login.email, 'access_token': access_token, 'expires': expires}

    def logout(self) -> dict:
        #current_user = self.repository.get(pk=get_jwt_identity())
        #access_token = get_raw_jwt()
        token_blacklisted = {
            #'token': access_token['jti'],
            #'expires': BlacklistToken().transform_expires_to_date(access_token['exp']),
            #'user_id': access_token['identity']
        }
        #token = BlacklistToken(**token_blacklisted)
        #token.add()
        #return {'code': 200, 'message': f'Successfully logout user {current_user.email}'}