import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user(client):
    response = client.post('/api/users', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
