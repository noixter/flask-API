from werkzeug.exceptions import HTTPException

from app.tests.tools.exceptions import BaseHTTPException


class ObjectNotFound(BaseHTTPException):
    status_code = 404
    default = 'Bad request'


class PermissionDenied(BaseHTTPException):
    status_code = 403
    default = 'Not allowed to perform this action'


class NotAuthenticated(BaseHTTPException):
    status_code = 401
    default = 'Not authentication method provided'
