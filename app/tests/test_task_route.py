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
        assigned_tasks=[]
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
        "assigned_tasks": []
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
        assigned_tasks=[]
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
        "assigned_tasks": []
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

