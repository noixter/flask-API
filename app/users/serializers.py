import re
from typing import Optional

from marshmallow import Schema, ValidationError, fields, post_load, validates

from app.users import ma
from app.users.models import Role, User

regex_names = r'[\W\d]'


def regex_validation_names(
    name: str,
    regex_expression: Optional[str] = None
) -> None:
    regex = regex_expression or regex_names
    if re.search(regex, name):
        raise ValidationError('No allowed meta characters or digits on string ')


class RoleSerializer(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
        include_fk = False


class UserSerializer(ma.SQLAlchemyAutoSchema):

    email = fields.Email()
    role = fields.Nested(RoleSerializer(only=["name"]))

    class Meta:
        model = User
        include_fk = True
        ordered = True

    @validates('first_name')
    def validate_first_name(self, first_name):
        regex_validation_names(first_name)
        return first_name.lower().capitalize()

    @validates('last_name')
    def validate_last_name(self, last_name):
        regex_validation_names(last_name)
        return last_name.lower().capitalize()

    @post_load
    def change_rol_id(self, data, **kwargs):
        if not data.get('role_id'):
            return data

        role = Role.query.get(data.get('role_id'))
        if not role:
            raise ValidationError('Role not found', 'role')

        data['role_id'] = role.id
        return data


class LoginSerializer(Schema):

    user_id = fields.Integer()
    password = fields.String()
