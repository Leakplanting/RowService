from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus, quote, urlparse, parse_qs, urlencode

load_dotenv()
app = Flask(__name__)
CORS(app)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5001))

def get_db():
    mongodb_uri = os.getenv("MONGODB_CONN")
    if not mongodb_uri:
        raise ValueError("MONGODB_CONN environment variable is not set")
    
    # Sanitize and use the MongoDB URI
    sanitized_uri = sanitize_mongodb_uri(mongodb_uri)
    client = MongoClient(sanitized_uri)
    return client.Leakplanting

def sanitize_mongodb_uri(uri):
    # Parse the URI into components
    parsed = urlparse(uri)
    
    # Extract the base URI (everything before the query parameters)
    base_uri = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    # Parse query parameters
    params = parse_qs(parsed.query)
    
    # Convert parameters to single values (not lists)
    params = {k: v[0] for k, v in params.items()}
    
    # Add or update required parameters
    params.update({
        'retryWrites': 'true',
        'w': 'majority',
        'tls': 'true'
    })
    
    # Reconstruct the URI
    query_string = urlencode(params)
    return f"{base_uri}?{query_string}"

@app.route('/fields', methods=['GET'])
def get_all_fields():
    db = get_db()
    fields = db.Fields.find()
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