from . import db


class Reading(db.Model):
    __tablename__ = 'readings'

    id = db.Column(db.Integer, primary_key=True)
    devEUI = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.Integer, nullable=False)
    payload = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return 'id={}, devEUI={}, port={}, datetime={}, payload={}'.format(self.id, self.devEUI,
                                                                           self.port, self.datetime, self.payload)