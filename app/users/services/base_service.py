from abc import ABC, abstractmethod
from typing import Optional

from flask import Request

from app.users.models import User


class UserServices(ABC):

    @abstractmethod
    def create_access_token(self, user_id: int):
        """Create a user access token"""


class AuthServices(ABC):

    @abstractmethod
    def validate(self, request: Optional[Request] = None) -> User:
        """Validate an existing token or credentials"""
