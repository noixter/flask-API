import random
from typing import Any, Dict, List, Optional

from faker import Faker

from app.users.models import Role, User
from users import models as domain_models
from users.exceptions import ObjectNotFound
from users.repositories.base_interface import RoleRepository, UserRepository

faker = Faker()


def create_roles() -> List[Role]:
    names = [(1, 'user'), (2, 'admin')]
    roles = [
        Role(id=id_, name=name)
        for id_, name in names
    ]
    return roles


def create_test_user() -> User:
    user = domain_models.User(
        id=faker.pyint(),
        first_name=faker.name(),
        last_name=faker.name(),
        email=faker.email(),
        role_id=random.choice([1, 2])
    )
    return user


class FakeRoleRepository(RoleRepository):

    def __init__(self, roles: Optional[List[Role]] = None):
        self.roles: List[Role] = roles or create_roles()

    def get(self, id_: int) -> Optional[Role]:
        role = [
            role
            for role in self.roles
            if role.id == id_
        ]
        if role:
            return self.to_domain(role[0])

    def add(self, id_: int, name: str) -> Role:
        role = Role(id=id_, name=name)
        self.roles.append(role)
        return self.to_domain(role)

    @staticmethod
    def to_domain(model: Role) -> domain_models.Role:
        return domain_models.Role(
            id=model.id,
            name=model.name
        )


class FakeUserRepository(UserRepository):

    def __init__(self, users: Optional[List[User]] = None):
        self.users: List[User] = users or [create_test_user()]

    def get(self, pk: int) -> Optional[domain_models.User]:
        user = [
            user
            for user in self.users
            if user.id == pk
        ]
        if user:
            return self.to_domain(user[0])

    def list(self) -> List[domain_models.User]:
        return [
            self.to_domain(user)
            for user in self.users
        ]

    def add(self, data: Dict[str, Any]) -> domain_models.User:
        user = User(**data)
        self.users.append(user)
        return self.to_domain(user)

    def modify(
        self,
        pk: int,
        update_fields: Dict[str, Any]
    ) -> Optional[domain_models.User]:
        user = self.get(pk)
        if user:
            self.users.remove(user)
            for field in update_fields:
                if not hasattr(user, field):
                    continue
                setattr(user, field, update_fields[field])
            self.users.append(user)
            return self.to_domain(user)

    def delete(self, pk: int) -> None:
        user = self.get(pk)
        if not user:
            raise ObjectNotFound(f'User with id {pk} does not exists')
        [
            self.users.remove(user)
            for user in self.users
            if user.id == pk
        ]

    def filter_by_email(self, email: str) -> Optional[User]:
        user = [
            user
            for user in self.users
            if user.email == email
        ]
        if user:
            return self.to_domain(user[0])

    @staticmethod
    def to_domain(model: User) -> domain_models.User:
        return domain_models.User(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            password=model.password,
            role_id=model.role_id
        )
