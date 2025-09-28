import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tasks' in data
    assert len(data['tasks']) >= 0

def test_create_task(client):
    task_data = {"task": "Test task"}
    response = client.post('/tasks', 
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['task'] == 'Test task'
    assert data['done'] == False

def test_update_task(client):
    # First create a task
    task_data = {"task": "Test task for update"}
    create_response = client.post('/tasks', 
                                 data=json.dumps(task_data),
                                 content_type='application/json')
    created_task = json.loads(create_response.data)

    # Update the task
    update_data = {"done": True}
    response = client.put(f'/tasks/{created_task["id"]}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['done'] == True
