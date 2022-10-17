from abc import ABC, abstractmethod

from flask import Request

from users.constants import RoleTypes


class BasePermission(ABC):

    @abstractmethod
    def has_permission(
        self,
        request: Request
    ) -> bool:
        """Validates if an object has a certain permission"""


class AdminUser(BasePermission):

    def has_permission(
        self,
        request: Request
    ) -> bool:
        if request.user.role_id != RoleTypes.ADMIN.value:
            return False
        return True


class IsOwnUser(BasePermission):

    def has_permission(
        self,
        request: Request
    ) -> bool:
        path_parameter = request.path.rsplit('/', 1)[1]
        if not path_parameter:
            return False
        path_parameter = int(path_parameter)
        if not request.user.id == path_parameter:
            return False
        return True
