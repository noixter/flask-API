from enum import Enum, auto

from decouple import config


class RoleTypes(Enum):

    ADMIN = auto()
    REGULAR = auto()


class TokenTypes(Enum):

    ACCESS = dict(
        type_='access',
        expiration=config('ACCESS_EXPIRATION_TIME', 12)
    )
    REFRESH = dict(
        type_='refresh',
        expiration=config('REFRESH_EXPIRATION_TIME', 13)
    )
