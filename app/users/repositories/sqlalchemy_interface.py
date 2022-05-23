from typing import Dict, Any, List, Optional
from app.users.repositories.base_interface import UserRepository
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from app.users.models import User


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get(self, pk: int) -> Optional[User]:
        user = User.query.get(pk)
        if not user:
            return None
        return user

    def list(self) -> List[User]:
        return User.query.all()

    def add(self, data: Dict[str, Any]) -> User:
        user = self.filter_by_email(email=data.get('email', ''))
        if not user:
            user = User(**data)
            try:
                self.db.session.add(user)
            except (IntegrityError, FlushError):
                raise Exception(f'User {user.email} already exists')
            self.db.session.commit()
            return user
        return user

    def modify(
        self, pk: int,
        update_fields: Dict[str, Any]
    ) -> Optional[User]:
        user = self.get(pk=pk)
        if user:
            for field in update_fields:
                if not hasattr(user, field):
                    continue
                setattr(user, field, update_fields[field])
            self.db.session.commit()
            return user

    def delete(self, pk: int) -> None:
        user = self.get(pk=pk)
        if not user:
            try:
                self.db.session.delete(user)
            except IntegrityError:
                raise f'User {user.email} can not be deleted'
            self.db.session.commit()

    def filter_by_email(self, email: str) -> Optional[User]:
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return user
