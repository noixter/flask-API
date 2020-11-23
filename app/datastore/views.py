from . import datastore, db, client, broker
from .models import Reading
from flask import request, jsonify
from sqlalchemy.exc import DataError, IntegrityError
from flask_jwt_extended import jwt_required


mongodb = client['readings']  # database
mongo_readings = mongodb['readings']  # collection


@datastore.route('ingest', endpoint='ingest', methods=['POST'])
def ingest():
    """Principal Route for ingest data
        data structure represents a LoRaWAN json format
        principal parameters are: end_device_id, port, datetime, payload
        :return 200 if json format can be storage on database
                400 if anything wrong happens
    """
    print(request.json)
    data = {
        'eui': request.json.get('end_device_id'),
        'port': request.json.get('port'),
        'datetime': request.json.get('received_time'),
        'payload': request.json.get('payload')
    }

    reading = broker.send_task('main.lora_process', (data,))
    if reading.ready():
        return jsonify(message='Receive'), 200
    else:
        return jsonify(error='Something goes wrong'), 400


@datastore.route('<deveui>/get_data', endpoint='get_sensor_data', methods=['GET'])
@jwt_required
def get_sensor_data(deveui):
    """Route for getting data from specific devEUI sensor
        :param deveui sensor identifier
        :return json response with all readings
    """
    data = Reading.get_delete_put_post(prop_filters={'eui': deveui})
    return jsonify(count=len(data.json), data=data.json)


@datastore.route('get_data', endpoint='get_data', methods=['GET'])
@jwt_required
def get_data():
    """Get all the storage data from all the sensors
        :return json list with all the data storage and a count of those
    """
    data = Reading.get_delete_put_post()
    return jsonify(count=len(data.json), data=data.json)
