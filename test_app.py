from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_api_put_customers():
    response = client.post('/api/move/customer')
    assert response.json() == {'message': 'success'}

