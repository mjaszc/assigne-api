import pytest
import datetime
from fastapi import HTTPException

import app.models.project_model as project_model
import app.crud.project_crud as project_crud
import app.schemas.project_schema as project_schema
import app.schemas.user_schema as user_schema
import app.models.user_model as user_model
import app.crud.user_crud as user_crud


# CRUD DATABASE OPERATIONS FOR PROJECT 


# CREATE PROJECT
def test_create_project(session):
    user = user_schema.UserCreate(username="test_user", email="test_email@example.com", password="test_password")
    user = user_crud.create_user(session, user)

    project = project_schema.ProjectCreate(name="test_project", description="test_description")
    created_project = project_crud.create_project(session, project, user)
    assert created_project.name == project.name
    assert created_project.description == project.description
    assert created_project.start_date == datetime.date.today()
    assert created_project.author_id == user.id

    # Try to create project with the same name
    with pytest.raises(HTTPException):
        project_crud.create_project(session, project, user)

# UPDATE PROJECT
def test_update_project(session):
    test_project = project_model.Project(
        id=1,
        name="Test Project",
        description="This is a test project.",
        start_date="2023-06-20",
        author=user_model.User(
            id=1,
            email="user@example.com",
            username="string",
            is_active=True,
            assigned_tasks=[]
        ),
        assigned_users=[]
    )

    session.add(test_project)
    session.commit()

    updated_data = {"name": "Updated Project Name", "description": "This is the updated project description."}
    updated_project = project_schema.ProjectUpdate(**updated_data)
    updated_project = project_crud.update_project(session, test_project.id, updated_project)

    # Check that the updated project has the correct data
    assert updated_project.name == "Updated Project Name"
    assert updated_project.description == "This is the updated project description."

    # Check that the database has also been updated with the new data
    session.refresh(test_project)
    assert test_project.name == "Updated Project Name"
    assert test_project.description == "This is the updated project description."

    session.delete(test_project)
    session.commit()

# GET PROJECT BY ID
def test_get_project_by_id(session):
    user = user_schema.UserCreate(username="test_user", email="test_email@example.com", password="test_password")
    user = user_crud.create_user(session, user)

    project = project_schema.ProjectCreate(name="test_project", description="test_description")
    created_project = project_crud.create_project(session, project, user)
    project_id = created_project.id
    response = project_crud.get_project(session, project_id)

    assert response.id == created_project.id
    assert response.name == created_project.name
    assert response.description == created_project.description
    assert response.start_date == created_project.start_date
    assert response.author == user
    assert response.assigned_users == []


# GET ALL PROJECTS
def test_get_all_projects(session):
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

# DELETE PROJECT
def test_delete_project(session):
    test_project = project_model.Project(
        id=1,
        name="Test Project",
        description="This is a test project.",
        start_date="2023-06-20",
        author=user_model.User(
            id=1,
            email="user@example.com",
            username="string",
            is_active=True,
            assigned_tasks=[]
        ),
        assigned_users=[]
    )

    session.add(test_project)
    session.commit()

    result = project_crud.delete_project(session, test_project.id)
    assert result is True
    assert session.query(project_model.Project).filter(project_model.Project.id == test_project.id).first() is None

    # Test deleting non-existent project
    result = project_crud.delete_project(session, test_project.id)
    assert result is False
