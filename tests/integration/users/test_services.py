import random

import pytest
from faker import Faker

from shared.tools.pyjwt import JWTHandler
from tests.integration.users.setup_services import (FakeRoleRepository,
                                                    FakeUserRepository)
from users.exceptions import NotAuthenticated, ObjectNotFound, ValidationError
from users.repositories.base_interface import RoleRepository, UserRepository
from users.services.base import LoginServices
from users.services.services import JWTLogin, UserServices

faker = Faker()


class TestLoginServices:

    users: UserRepository = FakeUserRepository()
    service: LoginServices = JWTLogin(
        repository=users,
        token_handler=JWTHandler()
    )

    def test_login_a_user(self):
        user = self.users.list()[0]
        tokens = self.service.login(user_id=user.id, password=user.password)
        assert tokens.get('access_token')
        assert tokens.get('refresh_token')

    def test_login_with_incorrect_credentials(self):
        user = self.users.list()[0]
        with pytest.raises(NotAuthenticated):
            self.service.login(user_id=user.id, password=faker.pystr())

    def test_login_a_non_existing_user(self):
        with pytest.raises(ObjectNotFound):
            self.service.login(
                user_id=faker.user_name(),
                password=faker.pystr()
            )


class TestUserServices:

    users: UserRepository = FakeUserRepository()
    roles: RoleRepository = FakeRoleRepository()
    services = UserServices(
        user_repository=users,
        role_repository=roles
    )

    def test_create_a_user_successfully(self):
        user_data = {
            "first_name": faker.name(),
            "last_name": faker.name(),
            "email": faker.email(),
            "password": faker.pystr(),
            "role_id": random.choice([1, 2])
        }
        self.services.create_user(user_data)
        assert len(self.users.list()) > 1
        user = self.users.filter_by_email(user_data.get('email'))
        assert user.first_name == user_data.get('first_name')
        assert user.last_name == user_data.get('last_name')
        rol = self.roles.get(user_data.get('role_id'))
        assert rol
        assert rol.id == user_data.get('role_id')

    def test_create_an_existing_user(self):
        user = self.users.list()[0]
        with pytest.raises(ValidationError):
            self.services.create_user(user.__dict__)

    def test_create_a_user_with_a_wrong_role(self):
        user = self.users.list()[0]
        user.rol_id = random.randint(0, 100)
        with pytest.raises(ValidationError):
            self.services.create_user(user.__dict__)

    def test_modify_a_user(self):
        existing_user = self.users.list()[0]
        modified_data = {
            'first_name': faker.name(),
            'last_name': faker.name()
        }
        self.services.modify_user(
            pk=existing_user.id, update_fields=modified_data
        )
        modified_user = self.users.get(pk=existing_user.id)
        assert modified_user.first_name == modified_data.get('first_name')
        assert modified_user.last_name == modified_data.get('last_name')

    def test_modify_a_non_existing_user(self):
        modified_data = {
            'first_name': faker.name(),
            'last_name': faker.name()
        }
        with pytest.raises(ValidationError):
            self.services.modify_user(pk=faker.pyint(), update_fields=modified_data)

    def test_delete_a_user(self):
        existing_user = self.users.list()[0]
        self.services.delete_user(pk=existing_user.id)
        assert not self.users.get(pk=existing_user.id)

    def test_delete_a_non_existing_user(self):
        with pytest.raises(ObjectNotFound):
            self.services.delete_user(pk=faker.pyint())
