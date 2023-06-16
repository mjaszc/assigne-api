from fastapi import status

def test_register_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testing"
    }

    response = client.post("/register", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": "testuser@example.com",
        "username": "testuser",
        "is_active": True,
        "id": 1,
        "assigned_tasks": []
    }
