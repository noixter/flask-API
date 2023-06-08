from datetime import datetime, timedelta
from typing import Union

from flask_jwt_extended.utils import create_access_token, get_jwt_identity, get_raw_jwt
from flask_restplus import abort
from flask_restplus.errors import ValidationError

from app.users.models import BlacklistToken, Users
from app.users.repositories.base_interface import UserRepositorie
from app.users.services.base_service import UserServices


class UserRestServices(UserServices):
    def __init__(self, user_repositorie: UserRepositorie):
        self.repositorie = user_repositorie

    def retrieve_user(self, pk: int) -> Union[Users, dict]:
        user = self.repositorie.get_user(pk)
        if not user:
            abort(404, code_error=400, message="User does not exist")
        return user

    def list_users(self):
        users = self.repositorie.list_users()
        return users

    def create_object(self, user_data: dict) -> dict:
        current_user = self.repositorie.get_user(pk=get_jwt_identity())

        if not current_user.rol_id == 1:
            abort(403, code_error=403, error="Not allowed to create new Users")

        if self.repositorie.filter_by_email(email=user_data.get("email")):
            abort(
                400,
                code_error=400,
                error=f'User with email {user_data.get("email")} already exist',
            )

        self.repositorie.create_object(user_data)
        return {"code": 201, "message": "created"}

    def modify_user(self, pk: int, update_fields: dict) -> Users:
        current_user = self.repositorie.get_user(pk=get_jwt_identity())
        user_to_update = Users.query.get(pk)

        if not user_to_update:
            abort(400, code_error=400, error="User does not exists")

        if not current_user.rol_id == 1 and not current_user == user_to_update:
            abort(403, code_error=403, error="Not allowed to change this user")

        try:
            user_to_update.update_object(update_fields)
            return {"code": 200, "message": "updated"}
        except ValidationError as e:
            abort(400, code_error=400, errors=e.messages)

    def delete_user(self, pk: int):
        current_user = self.repositorie.get_user(pk=get_jwt_identity())
        user_to_delete = self.repositorie.get_user(pk)
        if not user_to_delete:
            abort(400, code_error=400, error="User does not exists")

        if current_user.rol_id == 1 or current_user != user_to_delete:
            self.repositorie.delete_object(user_to_delete)
            return {"code": 200, "message": "deleted"}

    def login(self, params: dict) -> dict:
        if not params:
            abort(400, code_error=400, error="No username or password to authenticate")

        user_to_login = self.repositorie.filter_by_email(email=params.get("email"))

        if not user_to_login:
            abort(400, code_error=400, error="username does not exist")

        if not user_to_login.password == params.get("password"):
            abort(401, code_error=401, error="Username or password incorrect")

        access_token = create_access_token(identity=user_to_login.id)
        expires = datetime.timestamp(datetime.now() + timedelta(days=1))

        return {
            "user": user_to_login.email,
            "access_token": access_token,
            "expires": expires,
        }

    def logout(self) -> dict:
        current_user = Users.query.filter_by(id=get_jwt_identity()).first()
        access_token = get_raw_jwt()
        token_blacklisted = {
            "token": access_token["jti"],
            "expires": BlacklistToken().transform_expires_to_date(access_token["exp"]),
            "user_id": access_token["identity"],
        }
        token = BlacklistToken(**token_blacklisted)
        token.add()
        return {"code": 200, "message": f"Successfully logout user {current_user.email}"}
