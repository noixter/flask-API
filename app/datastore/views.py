from . import datastore, broker
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from celery.utils import gen_unique_id


# mongodb = client['readings']  # database
# mongo_readings = mongodb['readings']  # collection


@datastore.route('ingest', endpoint='ingest', methods=['POST'])
def ingest():
    """Principal Route for ingest data
        data structure represents a LoRaWAN json format
        principal parameters are: end_device_id, port, received_time and payload
        message are redirected to a AMQP message broker for decode and storage
        :return 200 if json format can be storage on database
    """

    data = {
        'end_device_id': request.json.get('end_device_id'),
        'port': request.json.get('port'),
        'received_time': request.json.get('received_time'),
        'payload': request.json.get('payload')
    }

    with broker:
        simple_queue = broker.SimpleQueue('LORA')
        simple_queue.put({'task': 'tasks.receive_messages',
                          'id': gen_unique_id(),
                          'args': [data]
                          })
        print(f'Sent: {data}')
        simple_queue.close()

    return jsonify(message='Receive'), 200


@datastore.route('<deveui>/get_data', endpoint='get_sensor_data', methods=['GET'])
@jwt_required
def get_sensor_data(deveui):
    """Route for getting data from specific devEUI sensor
        :param deveui sensor identifier
        :return json response with all readings
    """
    pass
    #data = Reading.get_delete_put_post(prop_filters={'eui': deveui})
    #return jsonify(count=len(data.json), data=data.json)


@datastore.route('get_data', endpoint='get_data', methods=['GET'])
@jwt_required
def get_data():
    """Get all the storage data from all the sensors
        :return json list with all the data storage and a count of those
    """
    pass
    #data = Reading.get_delete_put_post()
    #return jsonify(count=len(data.json), data=data.json)
