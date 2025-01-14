import pytest
from app import app, send_message_to_rabbitmq
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    # Testclient maken voor de Flask-app
    with app.test_client() as client:
        yield client

@patch('app.mongo')
@patch('app.send_message_to_rabbitmq')
def test_get_all_fields(mock_send_message, mock_mongo, client):
    # Mock de MongoDB-collectie
    mock_fields = [
        {
            '_id': '123',
            'Rows': ['row1', 'row2'],  # Minder dan 10 rijen
            'Fieldnumber': 1,
            'FieldName': 'Test Field'
        },
        {
            '_id': '124',
            'Rows': ['row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row10'],  # Exact 10 rijen
            'Fieldnumber': 2,
            'FieldName': 'Another Field'
        }
    ]
    mock_mongo.db.Fields.find.return_value = mock_fields

    # Maak een GET-verzoek naar de endpoint
    response = client.get('/fields')

    # Controleer de HTTP-statuscode
    assert response.status_code == 200

    # Controleer of de JSON-response klopt
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['fieldname'] == 'Test Field'
    assert data[1]['fieldname'] == 'Another Field'

    # Controleer dat het RabbitMQ-bericht werd verzonden voor velden met <10 rijen
    mock_send_message.assert_called_once_with({
        'field_id': '123',
        'fieldname': 'Test Field',
        'fieldnumber': 1,
        'row_count': 2
    })