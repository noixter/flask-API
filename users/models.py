from dataclasses import dataclass
from typing import Optional


@dataclass
class Role:
    id: int
    name: str

    def __repr__(self):
        return f'{self.id} -> {self.name}'


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    email: str
    role_id: int
    password: Optional[str] = None

    def __repr__(self):
        return f'<{self.id} {self.first_name} {self.last_name}>'
