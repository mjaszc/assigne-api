from fastapi import status
from unittest.mock import MagicMock
import app.crud.project_crud as project_crud
import app.models.project_model as project_model
import app.models.user_model as user_model
import app.crud.user_crud as user_crud

def test_create_project(client):
    mock_project = MagicMock(spec=project_model.Project)

    mock_create_project = MagicMock(return_value=mock_project)
    project_crud.create_project = mock_create_project

    mock_user = MagicMock(spec=user_model.User)
    mock_user.id = 1
    mock_user.email = "user@example.com"
    mock_user.username = "string"
    mock_user.is_active = True
    mock_user.assigned_tasks = []

    mock_get_current_user = MagicMock(return_value=mock_user)
    user_crud.get_current_user = mock_get_current_user

    mock_project.id = 1
    mock_project.name = "string1"
    mock_project.description = "string1"
    mock_project.start_date = "2023-06-20"
    mock_project.author = mock_user
    mock_project.assigned_tasks = []

    project_data = {
        "name": "Test Project",
        "description": "Test Test Test"
    }
    response = client.post("/api/v1/projects", json=project_data)

    assert response.status_code == status.HTTP_200_OK
    expected_data = {
        "name": mock_project.name,
        "description": mock_project.description,
        "id": mock_project.id,
        "start_date": mock_project.start_date,
        "author": {
            "email": mock_user.email,
            "username": mock_user.username,
            "is_active": mock_user.is_active,
            "id": mock_user.id,
            "assigned_tasks": mock_user.assigned_tasks
        },
        "assigned_tasks": mock_project.assigned_tasks
    }
    assert response.json() == expected_data
