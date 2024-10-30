from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import base64
app = Flask(__name__)
CORS(app)
# Configuratie voor MongoDB
import os
# Retrieves the hostname/IP address from the "HOST" environment variable.
HOST = os.getenv("HOST", "0.0.0.0")
# Retrieves the port number from the "PORT" environment variable, defaults to 5000 if not set.
PORT = int(os.getenv("PORT", 5000))
CONN = "mongodb+srv://jmanders07:Manders123.@cluster0.9rwq0.mongodb.net/Leakplanting?retryWrites=true&w=majority&appName=AtlasApp"
mongo = PyMongo(app, CONN, tlsAllowInvalidCertificates=True)

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
    app.run(host=HOST, port=PORT)
