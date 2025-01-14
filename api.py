from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
# import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()
mongodb_conn = os.getenv("MONGODB_CONN")
app = Flask(__name__)
CORS(app)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5001))
mongo = PyMongo(app, mongodb_conn, tlsAllowInvalidCertificates=True)

# RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

# def send_message_to_rabbitmq(message):
#     connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
#     channel = connection.channel()

#     channel.queue_declare(queue='notifications')

#     channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(message))
#     connection.close()

@app.route('/fields', methods=['GET'])
def get_all_fields():
    fields = mongo.db.Fields.find()
    fields_list = []

    for field in fields:
        field_data = {
            'id': str(field['_id']),
            'rows': field['Rows'],
            'fieldnumber': field['Fieldnumber'],
            'fieldname': field['FieldName'],
        }
        fields_list.append(field_data)

        # if len(field_data['rows']) < 10:
        #     message = {
        #         'field_id': field_data['id'],
        #         'fieldname': field_data['fieldname'],
        #         'fieldnumber': field_data['fieldnumber'],
        #         'row_count': len(field_data['rows']),
        #     }
        #     send_message_to_rabbitmq(message)

    return jsonify(fields_list)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)