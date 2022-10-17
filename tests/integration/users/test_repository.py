import random
from typing import List

import pytest
from faker import Faker

from app.users.adapters.repository import (SQLAlchemyRoleRepository,
                                           SQLAlchemyUserRepository)
from app.users.models import Role, User
from users.exceptions import ObjectNotFound
from users.repositories.base_interface import RoleRepository, UserRepository

faker = Faker()


@pytest.fixture
def repository(_db) -> UserRepository:
    repository = SQLAlchemyUserRepository()
    return repository


@pytest.fixture
def role_repository(_db) -> RoleRepository:
    return SQLAlchemyRoleRepository()


@pytest.fixture
def test_role(_db) -> Role:
    role = Role(id=faker.pyint(), name=random.choice(['user', 'admin']))
    _db.session.add(role)
    return role


@pytest.fixture
def test_user(_db) -> User:
    user = User(**user_data())
    _db.session.add(user)
    return user


def user_data():
    return dict(
        id=faker.pyint(),
        first_name=faker.name(),
        last_name=faker.name(),
        email=faker.email(),
        password=faker.pystr(),
        role_id=random.choice([1, 2])
    )


class TestRoleRepository:

    roles: List[str] = ['user', 'admin']

    def test_add_a_role(self, _db, role_repository):
        data = {
            'id_': faker.pyint(),
            'name': random.choice(self.roles)
        }
        role = role_repository.add(**data)
        role_saved = Role.query.get(role.id)
        assert role_saved.id == role.id
        assert role_saved.name == role.name

    def test_cant_add_a_existing_role(self, test_role, role_repository):
        data = {
            'id_': test_role.id,
            'name': test_role.name
        }
        role_repository.add(**data)
        assert len(role_repository.db.session.dirty) == 0

    def test_get_a_role(self, test_role, role_repository):
        role = role_repository.get(test_role.id)
        assert role.id == test_role.id
        assert role.name == test_role.name

    def test_get_a_non_existing_role(self, role_repository):
        role = role_repository.get(random.randint(100, 103))
        assert not role


class TestUserRepository:

    def test_get_a_user(self, repository, test_user):
        user = repository.get(pk=test_user.id)
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_a_not_existing_user(self, repository):
        user = repository.get(pk=random.randint(100, 105))
        assert not user

    def test_add_a_user(self, repository):
        user_info = user_data()
        user = repository.add(user_info)
        for key, value in user_info.items():
            if hasattr(user, key):
                assert value == getattr(user, key)
        users = repository.list()
        assert len(users) >= 1

    def test_modify_user(self, repository, test_user):
        updated_fields = dict(
            email=faker.email(),
            first_name=faker.name()
        )
        user = repository.modify(
            pk=test_user.id, update_fields=updated_fields
        )
        assert user.email == updated_fields.get('email')
        assert user.first_name == updated_fields.get('first_name')

    def test_modify_user_does_not_exists(self, repository):
        update_fields = dict(
            email=faker.email(),
            first_name=faker.name()
        )
        user = repository.modify(
            pk=random.randint(100, 105),
            update_fields=update_fields
        )
        assert not user

    def test_delete_user(self, repository, test_user):
        repository.delete(pk=test_user.id)
        user = repository.get(pk=test_user.id)
        assert not user

    def test_delete_non_existing_user(self, repository):
        with pytest.raises(ObjectNotFound):
            repository.delete(pk=random.randint(100, 105))
