from abc import ABC, abstractmethod
from typing import Optional, Union
from app.users.models import Users



class BaseRepositorie(ABC):

    @abstractmethod
    def get_user(self, pk:int) -> Union[Users, dict]:
        """Get a single user object"""

    @abstractmethod
    def filter_by_email(self, email: str) -> Union[Users, dict]:
        """Filter user object by email"""

    @abstractmethod
    def list_users(self):
        """List all saved users"""


class UserRepositorie(BaseRepositorie):

    @abstractmethod
    def create_object(self, user_data: dict):
        """create a user onject"""

    @abstractmethod
    def update_object(self, user: Users, updated_fields):
        """update a user object"""

    @abstractmethod
    def delete_object(self, user: Users):
        """delete a user object"""

    @abstractmethod
    def create_access_token(self, user: Users):
        """create a jwt access token to the given user"""