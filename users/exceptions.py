from shared.tools.exceptions import BaseHTTPException


class ValidationError(BaseHTTPException):
    status_code = 400
    default = 'Bad Request'


class ObjectNotFound(BaseHTTPException):
    status_code = 404
    default = 'Not Found'


class PermissionDenied(BaseHTTPException):
    status_code = 403
    default = 'Not allowed to perform this action'


class NotAuthenticated(BaseHTTPException):
    status_code = 401
    default = 'Not authentication method provided'
