import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_task(client):
    response = client.post('/tasks', json={'name': 'Test Task'})
    assert response.status_code == 201
    assert b'Task added!' in response.data

def test_get_tasks(client):
    client.post('/tasks', json={'name': 'Test Task'})
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_update_task(client):
    client.post('/tasks', json={'name': 'Test Task'})
    response = client.put('/tasks/0', json={'name': 'Updated Task'})
    assert response.status_code == 200
    assert b'Task updated!' in response.data

def test_delete_task(client):
    client.post('/tasks', json={'name': 'Test Task'})
    response = client.delete('/tasks/0')
    assert response.status_code == 200
    assert b'Task deleted!' in response.data

