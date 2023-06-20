from fastapi import status
from unittest.mock import MagicMock
import app.crud.project_crud as project_crud
import app.models.project_model as project_model

def test_create_project(client):
    mock_project = MagicMock(spec=project_model.Project)

    mock_create_project = MagicMock(return_value=mock_project)
    project_crud.create_project = mock_create_project

    mock_project.id = 1
    mock_project.name = "Test Project"
    mock_project.description = "Test Test Test"
    mock_project.start_date = "2023-06-19"
    mock_project.author_id = 1
    mock_project.assigned_tasks = []

    project_data = {
        "name": "Test Project",
        "description": "Test Test Test"
    }
    response = client.post("/api/v1/projects/?user_id=1", json=project_data)

    assert response.status_code == status.HTTP_200_OK
    expected_data = {
        "id": mock_project.id,
        "name": mock_project.name,
        "description": mock_project.description,
        "start_date": mock_project.start_date,
        "author_id": mock_project.author_id,
        "assigned_tasks": mock_project.assigned_tasks,
    }
    assert response.json() == expected_data
