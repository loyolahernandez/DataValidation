import pytest
from app import create_app, db
from app.models import Task

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task(client):
    response = client.post('/add', data={'title': 'Test Task'})
    assert response.status_code == 302  # Redirect after adding task
    with client.application.app_context():
        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None

def test_complete_task(client):
    with client.application.app_context():
        task = Task(title='Incomplete Task')
        db.session.add(task)
        db.session.commit()
    response = client.get(f'/complete/{task.id}')
    assert response.status_code == 302  # Redirect after completing task
    with client.application.app_context():
        task = Task.query.get(task.id)
        assert task.complete is True

def test_delete_task(client):
    with client.application.app_context():
        task = Task(title='Task to be deleted')
        db.session.add(task)
        db.session.commit()
    response = client.get(f'/delete/{task.id}')
    assert response.status_code == 302  # Redirect after deleting task
    with client.application.app_context():
        task = Task.query.get(task.id)
        assert task is None
