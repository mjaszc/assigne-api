import app.models.project_model as project_model
import app.crud.project_crud as project_crud
import app.schemas.project_schema as project_schema
import app.schemas.user_schema as user_schema
import app.models.user_model as user_model

# CRUD DATABASE OPERATIONS FOR PROJECT 


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


# UPDATE PROJECT
def test_update_project_db(session):
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

    # check that the updated project has the correct data
    assert updated_project.name == "Updated Project Name"
    assert updated_project.description == "This is the updated project description."

    # Check that the database has also been updated with the new data
    session.refresh(test_project)
    assert test_project.name == "Updated Project Name"
    assert test_project.description == "This is the updated project description."

    session.delete(test_project)
    session.commit()


# GET ALL PROJECTS
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

