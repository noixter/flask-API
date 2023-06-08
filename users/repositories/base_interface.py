from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from flask_sqlalchemy import SQLAlchemy

from users.models import Role, User


class RoleRepository(ABC):

    db: SQLAlchemy

    @abstractmethod
    def get(self, id_: int) -> Optional[Role]:
        ...

    @abstractmethod
    def add(self, id_: int, name: str) -> Role:
        ...


class UserRepository(ABC):

    db: SQLAlchemy

    @abstractmethod
    def get(self, pk: int) -> Optional[User]:
        """Get a single user object"""

    @abstractmethod
    def list(self) -> List[User]:
        """List all saved users"""

    @abstractmethod
    def add(self, data: Dict[str, Any]) -> User:
        """Create a user object"""

    @abstractmethod
    def modify(
        self, pk: int,
        update_fields: Dict[str, Any]
    ) -> Optional[User]:
        """Modify user fields"""

    @abstractmethod
    def delete(self, pk: int) -> None:
        """Deletes a user object"""

    @abstractmethod
    def filter_by_email(self, email: str) -> User:
        """Find a user based on it's email"""
