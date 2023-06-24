from fastapi import status
from unittest.mock import MagicMock
import app.models.project_model as project_model
import app.crud.project_crud as project_crud
import app.schemas.project_schema as project_schema
import app.schemas.user_schema as user_schema
import app.models.user_model as user_model

# CRUD PROJECT

# CREATE PROJECT
def test_create_project_db(session):
    test_user = user_schema.User(
        username="test_user",
        email="test_user@example.com",
        password="test_password",
        id=1,
        is_active=True,
        assigned_tasks=[]
    )

    test_project = project_schema.ProjectCreate(
        name="Test Project",
        description="Test Description"
    )

    db_user = user_model.User(
        username="test_user",
        email="test_user@example.com",
        password="test_password",
        id=1,
        is_active=True
    )

    # Adding user to the database in order to assign him as a project author
    session.add(db_user)
    session.commit()

    project_crud.create_project(session, test_project, test_user)
    db_project = session.query(project_model.Project).filter(project_model.Project.name == test_project.name).first()
    assert db_project is not None

def test_create_project(client):
    project_data = {
        "name": "Test Project",
        "description": "Test Test Test"
    }

    mock_create_project = MagicMock(return_value = project_schema.Project(
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
        "name": "Test Project",
        "description": "Test Test Test",
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

# GET PROJECT BY ID
def test_get_project_by_id(client):
    mock_get_project = MagicMock(return_value=project_schema.Project(
        id=1,
        name="Test Project",
        description="Test Test Test",
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
    project_crud.get_project = mock_get_project

    response = client.get("/api/v1/projects/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "Test Project",
        "description": "Test Test Test",
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

# GET ALL PROJECTS
def test_get_all_projects(client, monkeypatch):
    mock_create_project_1 = MagicMock(return_value=project_schema.Project(
        id=1,
        name="Test Project One",
        description="Test Description One",
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

    mock_create_project_2 = MagicMock(return_value=project_schema.Project(
        id=2,
        name="Test Project Two",
        description="Test Description Two",
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

    def mock_get_all_projects(db, skip, limit):
        return [mock_create_project_1(), mock_create_project_2()]

    # Patch the project_crud.get_all_projects method to use the mock implementation
    monkeypatch.setattr(project_crud, "get_all_projects", mock_get_all_projects)

    response = client.get("/api/v1/projects/")
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            "id": 1,
            "name": "Test Project One",
            "description": "Test Description One",
            "start_date": "2023-06-20",
            "author": {
                "id": 1,
                "email": "user@example.com",
                "username": "string",
                "is_active": True,
                "assigned_tasks": []
            },
            "assigned_tasks": []
        },
        {
            "id": 2,
            "name": "Test Project Two",
            "description": "Test Description Two",
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
    ]

def test_get_all_projects_db(session):
    test_user = user_schema.User(
        username="test_user",
        email="test_user@example.com",
        password="test_password",
        id=1,
        is_active=True,
        assigned_tasks=[]
    )

    test_project_1 = project_schema.ProjectCreate(
        name="Test Project One",
        description="Test Description One"
    )

    test_project_2 = project_schema.ProjectCreate(
        name="Test Project Two",
        description="Test Description Two"
    )

    db_user = user_model.User(
        username="test_user",
        email="test_user@example.com",
        password="test_password",
        id=1,
        is_active=True
    )

    session.add(db_user)
    session.commit()

    project_crud.create_project(session, test_project_1, test_user)
    project_crud.create_project(session, test_project_2, test_user)

    project_crud.get_all_projects(session, 0, 100)
    db_projects = session.query(project_model.Project).offset(0).limit(100).all()
    assert db_projects is not None

# UPDATE PROJECT BY ID
def test_update_project_by_id(client):
    project_data = {
        "name": "Test Project",
        "description": "Test Test Test"
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
        "name": "Test Project",
        "description": "Test Test Test",
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

    updated_project_data = {
        "name": "Modified Project",
        "description": "Modified Project Description"
    }

    mock_update_project = MagicMock(return_value=project_schema.Project(
        id=1,
        name=updated_project_data["name"],
        description=updated_project_data["description"],
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
    project_crud.update_project = mock_update_project

    response = client.put("/api/v1/projects/1", json=updated_project_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "Modified Project",
        "description": "Modified Project Description",
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

