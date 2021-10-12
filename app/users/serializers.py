import re
from . import ma
from .models import Users, Role
from marshmallow import fields, validates, ValidationError, post_load

regex_names = r'[\W]'


class RoleSerializer(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
        include_fk = False


class UserSerializer(ma.SQLAlchemyAutoSchema):

    email = fields.Email()
    rol = fields.Nested(RoleSerializer(only=["name"]))

    class Meta:
        model = Users
        include_fk = True
        ordered = True

    @validates('first_name')
    def validate_first_name(self, first_name):
        if re.search(regex_names, first_name):
            raise ValidationError('No allowed metacaracters on string ')
        return first_name.lower().capitalize()

    @validates('last_name')
    def validate_last_name(self, last_name):
        if re.search(regex_names, last_name):
            raise ValidationError('No allowed metacaracters on string ')
        return last_name.lower().capitalize()

    @post_load
    def change_rol_id(self, data, **kwargs):
        if not data.get('rol'):
            return data

        try:
            rol_name = data['rol'].get('name').lower().capitalize()
        except AttributeError:
            raise ValidationError('Missing data for rol', 'rol')

        rol = Role.query.filter_by(name=rol_name).first()

        if not rol:
            raise ValidationError('Rol not found', 'rol')

        data['rol_id'] = rol.id
        data.pop('rol')

        return data