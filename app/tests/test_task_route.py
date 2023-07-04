from fastapi import status
from unittest.mock import MagicMock
import app.crud.project_crud as project_crud
import app.crud.task_crud as task_crud
import app.schemas.project_schema as project_schema
import app.schemas.task_schema as task_schema
import app.schemas.user_schema as user_schema

def test_create_task(client):
    project_data = {
        "name": "test_proj",
        "description": "test_desc"
    }

    mock_create_project = MagicMock(return_value=project_schema.Project(
        id=1,
        name=project_data["name"],
        description=project_data["description"],
        start_date="2023-06-20",
        author=user_schema.User(
            id=1,
            email="user@example.com",
            username="string",
            is_active=True,
            assigned_tasks=[]
        ),
        assigned_tasks=[],
        assigned_users=[]
    ))
    project_crud.create_project = mock_create_project

    response = client.post("/api/v1/projects", json=project_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "test_proj",
        "description": "test_desc",
        "start_date": "2023-06-20",
        "author": {
            "id": 1,
            "email": "user@example.com",
            "username": "string",
            "is_active": True,
            "assigned_tasks": []
        },
        "assigned_tasks": [],
        "assigned_users":[]
    }

    task_data = {
        "title": "test_task",
        "description": "test_desc"
    }

    mock_create_task = MagicMock(return_value=task_schema.Task(
        id=1,
        title="test_task",
        description="test_desc"
    ))

    task_crud.create_task = mock_create_task

    create_task_response = client.post("/api/v1/projects/1/tasks", json=task_data)
    assert create_task_response.status_code == status.HTTP_200_OK
    assert create_task_response.json() == {
        "title": "test_task",
        "description": "test_desc",
        "id": 1,
    }

def test_get_task(client):
    project_data = {
        "name": "test_proj",
        "description": "test_desc"
    }

    mock_create_project = MagicMock(return_value=project_schema.Project(
        id=1,
        name=project_data["name"],
        description=project_data["description"],
        start_date="2023-06-20",
        author=user_schema.User(
            id=1,
            email="user@example.com",
            username="string",
            is_active=True,
            assigned_tasks=[]
        ),
        assigned_tasks=[],
        assigned_users=[]
    ))
    project_crud.create_project = mock_create_project

    response = client.post("/api/v1/projects", json=project_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "test_proj",
        "description": "test_desc",
        "start_date": "2023-06-20",
        "author": {
            "id": 1,
            "email": "user@example.com",
            "username": "string",
            "is_active": True,
            "assigned_tasks": []
        },
        "assigned_tasks": [],
        "assigned_users": []
    }

    mock_get_task = MagicMock(return_value=task_schema.Task(
        id=1,
        title="test_task",
        description="test_desc"
    ))

    task_crud.get_task_by_id = mock_get_task

    response = client.get("/api/v1/projects/1/tasks/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": "test_task",
        "description": "test_desc",
        "id": 1,
    }

def test_update_task(client):
    project_data = {
        "name": "test_proj",
        "description": "test_desc"
    }

    mock_create_project = MagicMock(return_value=project_schema.Project(
        id=1,
        name=project_data["name"],
        description=project_data["description"],
        start_date="2023-06-20",
        author=user_schema.User(
            id=1,
            email="user@example.com",
            username="string",
            is_active=True,
            assigned_tasks=[]
        ),
        assigned_tasks=[],
        assigned_users=[]
    ))
    project_crud.create_project = mock_create_project
    project_crud.get_project = mock_create_project

    create_project_response = client.post("/api/v1/projects", json=project_data)
    assert create_project_response.status_code == status.HTTP_200_OK
    assert create_project_response.json() == {
        "id": 1,
        "name": "test_proj",
        "description": "test_desc",
        "start_date": "2023-06-20",
        "author": {
            "id": 1,
            "email": "user@example.com",
            "username": "string",
            "is_active": True,
            "assigned_tasks": []
        },
        "assigned_tasks": [],
        "assigned_users": []
    }

    task_data = {
        "title": "test_task",
        "description": "test_desc"
    }

    mock_create_task = MagicMock(return_value=task_schema.Task(
        id=1,
        title=task_data["title"],
        description=task_data["description"],
    ))

    task_crud.create_task = mock_create_task

    mock_proj = mock_create_project()
    mock_project_id = mock_proj.id
    create_task_response = client.post(f"/api/v1/projects/{mock_project_id}/tasks", json=task_data)
    assert create_task_response.status_code == status.HTTP_200_OK
    assert create_task_response.json() == {
        "title": "test_task",
        "description": "test_desc",
        "id": 1,
    }

    updated_task_data = {
        "title": "Updated task",
        "description": "This is updated task."
    }

    mock_updated_task = MagicMock(return_value=task_schema.Task(
        id=1,
        title=updated_task_data["title"],
        description=updated_task_data["description"]
    ))

    task_crud.update_task = mock_updated_task
    task_crud.get_task_by_id = mock_updated_task


    mock_task = mock_updated_task()
    mock_task_id = mock_task.id
    response = client.put(f"/api/v1/projects/{mock_project_id}/tasks/{mock_task_id}", json=updated_task_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Updated task",
        "description": "This is updated task."
    }

def test_delete_task(client):
    project_data = {
        "name": "test_proj",
        "description": "test_desc"
    }

    mock_create_project = MagicMock(return_value=project_schema.Project(
        id=1,
        name=project_data["name"],
        description=project_data["description"],
        start_date="2023-06-20",
        author=user_schema.User(
            id=1,
            email="user@example.com",
            username="string",
            is_active=True,
            assigned_tasks=[]
        ),
        assigned_tasks=[],
        assigned_users=[]
    ))
    project_crud.create_project = mock_create_project
    project_crud.get_project = mock_create_project

    create_project_response = client.post("/api/v1/projects", json=project_data)
    assert create_project_response.status_code == status.HTTP_200_OK
    assert create_project_response.json() == {
        "id": 1,
        "name": "test_proj",
        "description": "test_desc",
        "start_date": "2023-06-20",
        "author": {
            "id": 1,
            "email": "user@example.com",
            "username": "string",
            "is_active": True,
            "assigned_tasks": []
        },
        "assigned_tasks": [],
        "assigned_users": []
    }

    task_data = {
        "title": "Task to be removed",
        "description": "Description of task to be removed.",
    }

    mock_create_task = MagicMock(return_value=task_schema.Task(
        id=1,
        title=task_data["title"],
        description=task_data["description"],
    ))

    task_crud.create_task = mock_create_task

    mock_proj = mock_create_project()
    mock_project_id = mock_proj.id
    mock_task = mock_create_task()
    mock_task_id = mock_task.id

    create_task_response = client.post(f"/api/v1/projects/{mock_project_id}/tasks", json=task_data)
    assert create_task_response.status_code == status.HTTP_200_OK
    assert create_task_response.json() == {
        "title": "Task to be removed",
        "description": "Description of task to be removed.",
        "id": 1,
    }

    delete_response = client.delete(f"/api/v1/projects/{mock_project_id}/tasks/{mock_task_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
