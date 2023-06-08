from typing import Tuple

import pytest
from faker import Faker

from app.users.models import User
from shared.tools.pyjwt import JWTHandler, Token
from users.services.services import create_tokens

faker = Faker()


def create_user_data() -> User:
    user = User(
        id=faker.pyint(),
        first_name=faker.name(),
        last_name=faker.name(),
        email=faker.email(),
        password='1234',
        role_id=1
    )
    return user


@pytest.fixture
def create_admin_user(_db) -> User:
    user = create_user_data()
    _db.session.add(user)
    return user


@pytest.fixture
def create_normal_user(_db) -> User:
    user = create_user_data()
    user.role_id = 2
    _db.session.add(user)
    yield user


@pytest.fixture
def admin_authenticated(create_admin_user) -> Tuple[User, Token]:
    user = create_admin_user
    tokens = create_tokens(user_id=user.id, handler=JWTHandler())
    return user, tokens.get('access_token')


@pytest.fixture
def user_authenticated(create_normal_user) -> Tuple[User, Token]:
    user = create_normal_user
    tokens = create_tokens(user_id=user.id, handler=JWTHandler())
    return user, tokens.get('access_token')
