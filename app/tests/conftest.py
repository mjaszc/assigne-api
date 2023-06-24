import pytest
from fastapi.testclient import TestClient

from app.main import get_db, app
import app.db.database as database
from app.crud.user_crud import get_current_user

database.Base.metadata.drop_all(bind=database.engine)
database.Base.metadata.create_all(bind=database.engine)

@pytest.fixture()
def session():
    connection = database.engine.connect()
    transaction = connection.begin()
    session = database.SessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    def skip_auth():
        pass

    app.dependency_overrides[get_db] = override_get_db
    # Avoiding Bearer Authentication
    app.dependency_overrides[get_current_user] = skip_auth
    yield TestClient(app)
    del app.dependency_overrides[get_db]
    del app.dependency_overrides[get_current_user]
