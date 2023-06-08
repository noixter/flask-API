from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from flask import Request

from shared.tools.pyjwt import Token, TokenHandler
from users.models import User
from users.repositories.base_interface import UserRepository


class AuthServices(ABC):

    @abstractmethod
    def validate(
        self,
        request: Optional[Request] = None,
        **kwargs: Dict[str, Any]
    ) -> User:
        """Validate a http authorization method"""


class LoginServices(ABC):

    repository: UserRepository
    token_handler: TokenHandler

    @abstractmethod
    def login(self, user_id: int, **kwargs) -> Token:
        """Provides a login or authentication method to users"""
