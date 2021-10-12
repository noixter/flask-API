from . import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from datetime import datetime


class Role(db.Model):
    """Class Role
    @params: id autoincremental
    @params: name String
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.name)


class Users(db.Model):
    """Class Users, manage the general users"""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    rol = db.relationship('Role', backref=db.backref('Users', lazy=True))

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    # Helpers methods to manage db access

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


class BlacklistToken(db.Model):
    """Token blacklisted model"""

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    expires = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return '[{}]: {} > {}'.format(self.id, self.user_id, self.expires)

    @staticmethod
    def transform_expires_to_date(expires):
        return datetime.fromtimestamp(expires)

    # Manage add to db a token

    def add(self):
        db.session.add(self)
        db.session.commit()


