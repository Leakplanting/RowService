from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
# import pika
import json
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()
app = Flask(__name__)
CORS(app)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5001))

# RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
# def send_message_to_rabbitmq(message):
#     connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
#     channel = connection.channel()
#     channel.queue_declare(queue='notifications')
#     channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(message))
#     connection.close()

# Configure MongoDB
mongodb_uri = os.getenv("MONGODB_CONN")
if mongodb_uri:
    # Ensure the URI has the correct format
    if "?" in mongodb_uri:
        base_uri, options = mongodb_uri.split("?", 1)
        app.config["MONGO_URI"] = f"{base_uri}?tls=true&tlsAllowInvalidCertificates=true&{options}"
    else:
        app.config["MONGO_URI"] = f"{mongodb_uri}?tls=true&tlsAllowInvalidCertificates=true"
else:
    raise ValueError("MONGODB_CONN environment variable is not set")

mongo = PyMongo(app)

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

    return jsonify(fields_list)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)