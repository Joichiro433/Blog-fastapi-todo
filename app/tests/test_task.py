from fastapi.testclient import TestClient
from sqlmodel import Session

from models.task import Task


def test_create_task(client: TestClient):
    resp = client.post(
        url='/tasks/',
        json={'title': 'test task', 'done': False})
    data: dict = resp.json()

    assert resp.status_code == 200
    assert data == {'title': 'test task', 'done': False}


def test_read_tasks(session: Session, client: TestClient):
    task1 = Task(title='task1', done=False)
    task2 = Task(title='task2', done=True)
    session.add(task1)
    session.add(task2)
    session.commit()

    resp = client.get(url='/tasks/')
    data: list[dict] = resp.json()
    assert resp.status_code == 200
    assert len(data) == 2
    assert data[0] == {'title': 'task1', 'done': False, 'id': 1}
    assert data[1] == {'title': 'task2', 'done': True, 'id': 2}

    resp = client.get(
        url='/tasks/', 
        params={'done': True})
    data: list[dict] = resp.json()
    assert resp.status_code == 200
    assert len(data) == 1
    assert data[0] == {'title': 'task2', 'done': True, 'id': 2}

    resp = client.get(
        url='/tasks/', 
        params={'done': False})
    data: list[dict] = resp.json()
    assert resp.status_code == 200
    assert len(data) == 1
    assert data[0] == {'title': 'task1', 'done': False, 'id': 1}
    

def test_read_task(session: Session, client: TestClient):
    task1 = Task(title='task1', done=False)
    task2 = Task(title='task2', done=True)
    session.add(task1)
    session.add(task2)
    session.commit()

    resp = client.get(url='/tasks/1')
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {'title': 'task1', 'done': False, 'id': 1}

    resp = client.get(url='/tasks/2')
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {'title': 'task2', 'done': True, 'id': 2}

    resp = client.get(url='/tasks/3')
    assert resp.status_code == 404


def test_update_task(session: Session, client: TestClient):
    task1 = Task(title='task1', done=False)
    session.add(task1)
    session.commit()

    resp = client.patch(
        url='/tasks/1',
        json={'title': 'new task', 'done': True})
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {'title': 'new task', 'done': True, 'id': 1}

    resp = client.patch(
        url='/tasks/2',
        json={'title': 'new task', 'done': True})
    assert resp.status_code == 404


def test_delete_task(session: Session, client: TestClient):
    task1 = Task(title='task1', done=False)
    session.add(task1)
    session.commit()

    resp = client.delete(url='/tasks/1')
    assert resp.status_code == 200

    resp = client.get(url='/tasks/')
    data: list[dict] = resp.json()
    assert len(data) == 0
