# tests/test_app.py
from main import app

# Test if the index route returns a 200 status code
def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
