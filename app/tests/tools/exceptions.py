from typing import Optional, Dict, Any


class BaseHTTPException(Exception):
    status_code = 400
    default = 'Server received an unhandled request'

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        payload: Optional[Dict[str, Any]] = None
    ):
        self.message = message or self.default
        self.status_code = status_code or self.status_code
        self.payload = payload

    def to_dict(self):
        response = dict(self.payload or ())
        response['message'] = self.message
        response['code'] = self.status_code
        return response
