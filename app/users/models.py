from . import db
from flask_login import UserMixin
from flask_serialize import FlaskSerializeMixin


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

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_id(self):
        return self.user_id






