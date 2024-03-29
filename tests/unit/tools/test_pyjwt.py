import random
from datetime import datetime, timedelta

import jwt
import pytest
from faker import Faker

from shared.tools.pyjwt import JWTHandler

faker = Faker()


class TestPyJWT:

    jwt_client = JWTHandler()
    user_id = random.randint(0, 10)

    def test_create_a_token_successfully(self):
        expires_at = datetime.now() + timedelta(days=1)
        token = self.jwt_client.encode(user_id=self.user_id, expires_at=expires_at)
        assert token is not None
        assert type(token) == str
        headers = jwt.get_unverified_header(token)
        assert headers.get('alg') == self.jwt_client.algorithm
        assert headers.get('typ') == 'access'

    def test_decode_a_token_successfully(self):
        expires_at = datetime.now() + timedelta(days=1)
        token = self.jwt_client.encode(user_id=self.user_id, expires_at=expires_at)
        payload = self.jwt_client.decode(token)
        assert payload.get('user_id') == self.user_id
        exp = datetime.utcfromtimestamp(payload.get('exp'))
        assert exp == expires_at.replace(microsecond=0)

    def test_decode_a_expired_token(self):
        expires_at = datetime.now() - timedelta(days=2)
        token = self.jwt_client.encode(user_id=self.user_id, expires_at=expires_at)
        with pytest.raises(jwt.ExpiredSignatureError):
            self.jwt_client.decode(token)

    def test_decode_a_malformed_token(self):
        fake_client = jwt
        token = fake_client.encode(
            payload=dict(user_id=self.user_id),
            key=faker.pystr()
        )
        with pytest.raises(jwt.InvalidSignatureError):
            self.jwt_client.decode(token)

    def test_create_a_token_without_expiration_date(self):
        token = self.jwt_client.encode(self.user_id)
        payload = self.jwt_client.decode(token)
        assert not payload.get('exp')

    def test_create_a_token_with_extra_data(self):
        expires_at = datetime.now() + timedelta(days=1)
        name = faker.name()
        address = faker.address()
        extra_data = dict(name=name, address=address)
        token = self.jwt_client.encode(
            user_id=self.user_id,
            expires_at=expires_at,
            extra_data=extra_data
        )
        payload = self.jwt_client.decode(token)
        assert payload.get('name') == name
        assert payload.get('address') == address

    def test_create_a_refresh_token_type(self):
        expires_at = datetime.now() + timedelta(days=1)
        type_ = 'refresh'
        token = self.jwt_client.encode(
            user_id=self.user_id,
            type_=type_,
            expires_at=expires_at
        )
        headers = jwt.get_unverified_header(token)
        assert headers.get('typ') == 'refresh'
        assert headers.get('kid') is not None
