import re
from . import ma
from .models import Users
from marshmallow import fields, validates, ValidationError

regex_names = r'[\W]'

class UserSerializer(ma.SQLAlchemyAutoSchema):

    context = {}
    first_name = fields.String()
    last_name = fields.String()

    class Meta:
        model = Users
        include_fk = True
        fields = ('id', 'first_name', 'last_name', 'email', 'rol_id', 'position')

    def __init__(self):
        super(UserSerializer, self).__init__()
        print(self.context)
        try:
            if self.context['request'].method == 'POST':
                self.fields += 'password'
                self.fields += 'user_id'
        except KeyError:
            print('Sin request')

    @validates('first_name')
    def validate_first_name(self, first_name):
        if re.search(regex_names, first_name):
            raise ValidationError('No allowed metacaracters on string ')

    @validates('last_name')
    def validate_last_name(self, last_name):
        if re.search(regex_names, last_name):
            raise ValidationError('No allowed metacaracters on string ')


class UserPostSerializer(ma.SQLAlchemyAutoSchema):

    email = fields.Email()

    class Meta:
        model = Users
        include_fk = True

    @validates('first_name')
    def validate_first_name(self, first_name):
        if re.search(regex_names, first_name):
            raise ValidationError('No allowed metacaracters on string ')

    @validates('last_name')
    def validate_last_name(self, last_name):
        if re.search(regex_names, last_name):
            raise ValidationError('No allowed metacaracters on string ')