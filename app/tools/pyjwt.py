import importlib
from datetime import datetime
from typing import Union, Any, Optional, Dict, TypeVar
from uuid import uuid4

import jwt
from decouple import config


Token = TypeVar('Token')


class JWTHandler:

    def __init__(
        self, algorithm: Optional[str] = None,
        secret: Optional[str] = None
    ):
        try:
            importlib.import_module('jwt')
        except ImportError:
            raise f'{self.__name__} need a jwt library'
        self.algorithm = algorithm or config('JWT_ALGORITHM')
        self._secret = secret or config('SECRET_KEY')

    def encode(
        self,
        user_id: int,
        type_: Optional[str] = None,
        expires_at: Optional[Union[datetime, int]] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> Token:
        extra_data = extra_data or {}
        iat = datetime.now()
        typ = type_ or 'access'
        payload = {
            'user_id': user_id,
            'iat': iat
        }
        if expires_at:
            payload.update(exp=expires_at)
        payload |= extra_data
        headers = {
            'typ': typ,
            'alg': self.algorithm,
            'kid': uuid4().__str__()
        }
        token = jwt.encode(payload, self._secret, headers=headers)
        return token.decode('utf-8')

    def decode(self, token: str) -> Dict[str, Any]:
        headers = jwt.get_unverified_header(token)
        try:
            payload = jwt.decode(
                token, self._secret,
                algorithms=[headers.get('alg', self.algorithm)]
            )
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as e:
            raise e

    @staticmethod
    def get_token_headers(token: str) -> Dict[str, Any]:
        headers = jwt.get_unverified_header(token)
        return headers
