from datetime import datetime, timedelta
from typing import Union

from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.users.models import Users
from app.users.repositories.base_interface import UserRepositorie


class SQLAlchemyUser(UserRepositorie):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_user(self, pk: int) -> Union[Users, dict]:
        try:
            user = Users.query.get(pk)
            return user
        except NoResultFound:
            return {}

    def filter_by_email(self, email: str) -> Union[Users, dict]:
        try:
            user = Users.query.filter_by(email=email).first()
            return user
        except NoResultFound:
            return {}

    def list_users(self) -> list:
        users = Users.query.all()
        if not users:
            return []
        return users

    def create_object(self, user_data: dict):
        try:
            user = Users(**user_data)
            self.db.session.add(user)
        except (IntegrityError, FlushError):
            raise Exception(f"User {user.email} already exists")
        self.db.session.commit()

    def update_object(self, user: Users, updated_fields):
        for field in updated_fields:
            setattr(user, field, updated_fields[field])
        self.db.session.commit()

    def delete_object(self, user: Users):
        try:
            self.db.session.delete(user)
        except IntegrityError:
            raise Exception(f"User {user.email} can not be deleted")
        self.db.session.commit()

    def create_access_token(self, user: Users):
        access_token = create_access_token(identity=user.id)
        expires = datetime.timestamp(datetime.now() + timedelta(days=1))
        return {"access_token": access_token, "expires": expires}
