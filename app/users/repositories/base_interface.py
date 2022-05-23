from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.users.models import User


class UserRepository(ABC):

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
