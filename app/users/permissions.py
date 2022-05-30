from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

from flask import Request

from app.users.constants import RoleTypes
from app.users.models import User

_M = TypeVar('_M')


class BasePermission(ABC):

    @abstractmethod
    def has_permission(
        self,
        object_: Generic[_M],
        request: Optional[Request] = None
    ) -> bool:
        """Validates if an object has a certain permission"""


class AdminUser(BasePermission):

    def has_permission(
        self,
        object_: User,
        request: Optional[Request] = None
    ) -> bool:
        if object_.rol_id != RoleTypes.ADMIN.value:
            return False
        return True


class IsOwnUser(BasePermission):

    def has_permission(
        self,
        object_: User,
        request: Optional[Request] = None
    ) -> bool:
        path = request.path
        path_parameter = int(path.rsplit('/', 1)[1])
        if not object_.id == path_parameter:
            return False
        return True
