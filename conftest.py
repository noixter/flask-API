import os

import pytest

from app import configs, create_app
from app.users import db
from app.users.models import Role


@pytest.fixture(autouse=True, scope='session')
def _create_app(request):
    environment = configs.get('test')
    app = create_app(environment)
    context = app.app_context()
    context.push()

    def teardown():
        context.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def _db(_create_app, request):
    db.create_all()

    def teardown():
        db.session.rollback()
        db.drop_all()
        if os.path.exists('db_test.db'):
            os.remove('db_test.db')

    request.addfinalizer(teardown)
    return db


@pytest.fixture
def client(_create_app):
    return _create_app.test_client()


@pytest.fixture(autouse=True, scope='session')
def create_roles(_db):
    role_data = [
        Role(
            id=1,
            name='admin'
        ),
        Role(
            id=2,
            name='user'
        )
    ]
    for role in role_data:
        _db.session.add(role)
