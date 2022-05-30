from abc import ABC, abstractmethod
from typing import Optional, Any, Dict

from flask import Request

from app.users.models import User


class AuthServices(ABC):

    @abstractmethod
    def validate(
        self,
        request: Optional[Request] = None,
        **kwargs: Dict[str, Any]
    ) -> User:
        """Validate a http authorization method"""
