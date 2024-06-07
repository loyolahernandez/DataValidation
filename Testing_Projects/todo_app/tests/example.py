import pytest
import requests
from unittest.mock import patch
from app import create_app, db
from app.models import Task

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "CLOUD_SERVICE_URL": "https://mock-cloud-service.com",
        "CLOUD_SERVICE_API_KEY": "test-api-key"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.rollback()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@patch('requests.post')
def test_add_task(mock_post, client):
    # Mock response for cloud service validation
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"valid": true}'
    mock_post.return_value = mock_response
    
    response = client.post('/add', data={'title': 'Test Task'})
    assert response.status_code == 302  # Redirect after adding task

    with client.application.app_context():
        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None

@patch('requests.get')
def test_complete_task(mock_get, client):
    with client.application.app_context():
        task = Task(title='Incomplete Task')
        db.session.add(task)
        db.session.commit()

    # Mock response for cloud service update
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"complete": true}'
    mock_get.return_value = mock_response

    response = client.get(f'/complete/{task.id}')
    assert response.status_code == 302  # Redirect after completing task

    with client.application.app_context():
        task = Task.query.get(task.id)
        assert task.complete is True

@patch('requests.delete')
def test_delete_task(mock_delete, client):
    with client.application.app_context():
        task = Task(title='Task to be deleted')
        db.session.add(task)
        db.session.commit()

    # Mock response for cloud service deletion
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"deleted": true}'
    mock_delete.return_value = mock_response

    response = client.get(f'/delete/{task.id}')
    assert response.status_code == 302  # Redirect after deleting task

    with client.application.app_context():
        task = Task.query.get(task.id)
        assert task is None