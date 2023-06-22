from fastapi import status
from unittest.mock import MagicMock
import app.crud.user_crud as user_crud
import app.schemas.user_schema as user_schema
import app.models.user_model as user_model

def test_create_test_user_db(session):
    test_user = user_schema.UserCreate(
        username="test_user",
        email="test_user@example.com",
        password="test_password"
    )

    user_crud.create_user(session, test_user)

    db_user = session.query(user_model.User).filter(user_model.User.username == test_user.username).first()
    assert db_user is not None
    assert db_user.username == test_user.username
    assert db_user.email == test_user.email

def test_get_user_by_id(client):
    mock_get_user_by_id = MagicMock(return_value=user_schema.User(
            id=1,
            email="user@example.com",
            username="string",
            is_active=True,
            assigned_tasks=[]
    ))
    user_crud.get_user_by_id = mock_get_user_by_id

    response = client.get("/api/v1/users/1")

    assert response.status_code == status.HTTP_200_OK

    expected_data = {
        "id": 1,
        "email": "user@example.com",
        "username": "string",
        "is_active": True,
        "assigned_tasks": []
    }
    assert response.json() == expected_data

