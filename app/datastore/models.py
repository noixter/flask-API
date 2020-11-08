from . import db
from flask_serialize import FlaskSerializeMixin


class Reading(FlaskSerializeMixin, db.Model):
    __tablename__ = 'readings'

    id = db.Column(db.Integer, primary_key=True)
    eui = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.Integer, nullable=False)
    payload = db.Column(db.String(255), nullable=False)

    order_by_field = 'datetime'

    def __str__(self):
        return 'id={}, devEUI={}, port={}, datetime={}, payload={}'.format(self.id, self.eui,
                                                                           self.port, self.datetime, self.payload)