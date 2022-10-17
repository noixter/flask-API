from typing import Any, Dict, List, Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import FlushError

from app.users import db
from app.users.models import Role, User
from users import models as domain_models
from users.exceptions import ObjectNotFound
from users.repositories.base_interface import RoleRepository, UserRepository


class SQLAlchemyRoleRepository(RoleRepository):

    def __init__(self):
        self.db = db

    def get(self, id_: int) -> Optional[Role]:
        role = Role.query.get(id_)
        if role:
            return role

    def add(self, id_: int, name: str) -> Role:
        role = self.get(id_)
        if role:
            return self.to_domain(role)
        try:
            role = Role(id=id_, name=name)
            self.db.session.add(role)
        except SQLAlchemyError as e:
            raise Exception(str(e))

        return role

    @staticmethod
    def to_domain(model: Role) -> domain_models.Role:
        return domain_models.Role(
            id=model.id,
            name=model.name
        )


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self):
        self.db = db

    def get(self, pk: int) -> Optional[User]:
        user = User.query.get(pk)
        if user:
            return user

    def list(self) -> List[User]:
        return User.query.all()

    def add(self, data: Dict[str, Any]) -> User:
        user = User(**data)
        try:
            self.db.session.add(user)
        except (IntegrityError, FlushError):
            raise Exception(f'User {user.email} already exists')
        self.db.session.commit()
        return self.to_domain(user)

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
            return self.to_domain(user)

    def delete(self, pk: int) -> None:
        user = User.query.filter_by(id=pk).first()
        if not user:
            raise ObjectNotFound(f'User with id {pk} does not exists')
        try:
            self.db.session.delete(user)
            self.db.session.commit()
        except IntegrityError:
            raise ObjectNotFound(f'User {user.email} can not be deleted')

    def filter_by_email(self, email: str) -> Optional[User]:
        user = User.query.filter_by(email=email).first()
        if user:
            return user

    @staticmethod
    def to_domain(model: User) -> domain_models.User:
        return domain_models.User(
            id=model.id if getattr(model, 'id') else None,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            password=model.password,
            role_id=model.role_id
        )
