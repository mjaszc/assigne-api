from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import pytest
import os
from app.main import get_db, app
import app.db.database as database

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database.Base.metadata.drop_all(bind=engine)
database.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = SessionTest()
        yield db
    finally:
        db.close()

@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTest(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
