import app.schemas.task_schema as task_schema
import app.crud.task_crud as task_crud
import app.models.project_model as project_model
import app.models.user_model as user_model

# CRUD DATABASE OPERATIONS FOR TASK 

# CREATE TASK
def test_create_task(session):
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

    task = task_schema.TaskCreate(title="test_task", description="test_description")
    created_task = task_crud.create_task(session, task, test_project.id)
    assert created_task.title == task.title
    assert created_task.description == task.description


# GET TASK BY ID
def test_get_task_by_id(session):
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

    task = task_schema.TaskCreate(title="test_task", description="test_description")
    created_task = task_crud.create_task(session, task, test_project.id)
    assert created_task.title == task.title
    assert created_task.description == task.description

    get_task = task_crud.get_task_by_id(session, created_task.id, test_project.id)
    assert get_task.title == created_task.title
    assert get_task.description == created_task.description
