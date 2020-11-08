from . import datastore, db
from .models import Reading
from flask import request, jsonify
from sqlalchemy.exc import DataError, IntegrityError


@datastore.route('/')
def index():
    return 'welcome to datastore api'


@datastore.route('ingest', endpoint='ingest', methods=['POST'])
def ingest():
    print(request.json)
    data = {
        'devEUI': request.json.get('end_device_id'),
        'port': request.json.get('port'),
        'datetime': request.json.get('received_time'),
        'payload': request.json.get('payload')
    }

    reading = Reading(**data)
    try:
        db.session.add(reading)
        db.session.commit()
        return jsonify(message='added'), 200
    except (DataError, IntegrityError):
        print("data error")
        return jsonify(error='Something goes wrong'), 400
