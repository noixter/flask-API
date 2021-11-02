from abc import ABC, abstractmethod
from typing import Union

from app.users.models import Users


class UserServices(ABC):

    @abstractmethod
    def retrieve_user(self, pk: int) -> Union[Users, dict]:
        """retrieve a single user object"""

    @abstractmethod
    def list_users(self):
        """Get all saved users"""

    @abstractmethod
    def create_object(self, user_data: dict) -> dict:
        """Create a user object"""

    @abstractmethod
    def modify_user(self, pk: int, update_fields: dict) -> Users:
        """Patch a single user object""" 
    
    @abstractmethod
    def delete_user(self, pk: int):
        """Delete a single user object"""

    @abstractmethod
    def login(self, params: dict) -> dict:
        """Login a user object a retrieve its access token"""

    @abstractmethod
    def logout(self) -> dict:
        """logout a user"""

