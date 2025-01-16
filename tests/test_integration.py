import pytest
from api import app
import json
from bson import ObjectId
from unittest.mock import MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_fields(client, monkeypatch):
    # Mock data that we expect from MongoDB
    mock_fields = [
        {
            '_id': ObjectId('65a5307c1234567890abcdef'),
            'Rows': 10,
            'Fieldnumber': 1,
            'FieldName': 'Test Field 1'
        },
        {
            '_id': ObjectId('65a5307c0987654321fedcba'),
            'Rows': 15,
            'Fieldnumber': 2,
            'FieldName': 'Test Field 2'
        }
    ]

    # Create a mock collection
    mock_collection = MagicMock()
    mock_collection.find.return_value = mock_fields

    # Create a mock db
    mock_db = MagicMock()
    mock_db.Fields = mock_collection

    # Patch the db object in the api module
    monkeypatch.setattr('api.db', mock_db)

    # Make request to the endpoint
    response = client.get('/fields')
    
    # Check response status code
    assert response.status_code == 200
    
    # Parse response data
    data = json.loads(response.data)
    
    # Verify the structure and content of the response
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Check the first field
    assert data[0]['id'] == str(mock_fields[0]['_id'])
    assert data[0]['rows'] == mock_fields[0]['Rows']
    assert data[0]['fieldnumber'] == mock_fields[0]['Fieldnumber']
    assert data[0]['fieldname'] == mock_fields[0]['FieldName']
    
    # Check the second field
    assert data[1]['id'] == str(mock_fields[1]['_id'])
    assert data[1]['rows'] == mock_fields[1]['Rows']
    assert data[1]['fieldnumber'] == mock_fields[1]['Fieldnumber']
    assert data[1]['fieldname'] == mock_fields[1]['FieldName']

#$ python3 -m pytest tests/test_integration.py -v to run test