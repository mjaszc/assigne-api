from fastapi import status
from unittest.mock import MagicMock
import app.crud.user_crud as user_crud
import app.models.user_model as user_model

def test_get_user_by_id(client):
    mock_user = MagicMock(spec=user_model.User)

    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.is_active = True
    mock_user.assigned_tasks = []

    mock_get_user_by_id = MagicMock(return_value=mock_user)
    user_crud.get_user_by_id = mock_get_user_by_id

    mock_get_current_user = MagicMock(return_value=mock_user)
    user_crud.get_current_user = mock_get_current_user

    response = client.get("/api/v1/users/1")

    assert response.status_code == status.HTTP_200_OK

    expected_data = {
        "id": mock_user.id,
        "username": mock_user.username,
        "email": mock_user.email,
        "is_active": mock_user.is_active,
        "assigned_tasks": mock_user.assigned_tasks,
    }
    assert response.json() == expected_data

