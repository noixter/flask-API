from . import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from flask_login import UserMixin


class Role(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.name)


class Users(UserMixin, db.Model):
    """Class Users, manage the general users
        extends UserMixin for implements flask-login
        add attributes: is_active, is_authenticated for manage session
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(80), nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    rol = db.relationship('Role', backref=db.backref('Users', lazy=True))

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_id(self):
        return self.user_id

    def create_object(self):
        try:
            db.session.add(self)
        except (IntegrityError, FlushError):
            raise Exception('User {} already exists'.format(self))
        db.session.commit()

    def update_object(self, updated_fields):
        for field in updated_fields:
            setattr(self, field, updated_fields[field])
        db.session.commit()

    def delete_user(self):
        try:
            db.session.delete(self)
        except IntegrityError:
            raise Exception('User {} can not be deleted'.format(self))
        db.session.commit()








