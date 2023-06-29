import app.schemas.task_schema as task_schema
import app.crud.task_crud as task_crud
import app.models.project_model as project_model
import app.models.user_model as user_model
import app.models.task_model as task_model

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

def test_update_task(session):
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

    test_task = task_model.Task(
        id = 1,
        title = "test_task",
        description = "test_description",
        project_id = 1
    )

    session.add(test_task)
    session.commit()

    updated_task_data = {"title": "Updated Task Name", "description": "This is the updated task description."}
    updated_task = task_schema.TaskBase(**updated_task_data)
    task_crud.update_task(session, test_task.id , updated_task, test_project.id)

    session.refresh(test_task)
    assert test_task.title == "Updated Task Name"
    assert test_task.description == "This is the updated task description."