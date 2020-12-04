from . import db
from flask import request
from flask_login import UserMixin, current_user
from flask_serialize import FlaskSerializeMixin

FlaskSerializeMixin.db = db


class Role(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.name)


class Users(UserMixin, FlaskSerializeMixin, db.Model):
    """Class Users, manage the general users
        extends UserMixin for implements flask-login
        add attributes: is_active, is_authenticated for manage session
    """

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255))
    position = db.Column(db.String(80), nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    rol = db.relationship('Role', backref=db.backref('Users', lazy=True))

    exclude_serialize_fields = ['is_anonymous', 'is_authenticated', 'is_active', 'password']
    create_fields = ['user_id', 'first_name', 'last_name', 'email', 'password', 'position', 'rol_id']
    update_fields = ['user_id', 'first_name', 'last_name', 'email', 'password', 'position', 'rol_id']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_id(self):
        return self.user_id

    def can_access(self):
        """Authentication Method
            :returns: True if is admin or if method are GET, POST, PUT only if current user
            is equal to item to update
            :returns: False if method is DELETE and is the same user
            and every case else
        """
        if current_user.rol_id == 1:
            return True
        elif request.method == 'GET':
            return True
        elif request.method == ('POST' or 'PUT') and current_user == self:
            return True
        elif request.method == 'DELETE' and current_user.user_id == self.user_id:
            return False
        else:
            return False

    def can_delete(self):
        """Only admins can DELETE
            :throws: Exception if its other kind of user
        """
        if current_user.rol_id == 1:
            return True
        elif current_user == self:
            raise Exception('Not Allowed delete yourself')
        else:
            raise Exception('Delete Not Allowed')







