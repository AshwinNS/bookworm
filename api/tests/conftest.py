from os import environ as os_environ
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlmodel import Session, SQLModel, create_engine

from api.db import get_session
from api.main import app
from api.models import User, UserCreate

TEST_DATABASE_URL = f"{os_environ.get("DB_ENGINE")}://{os_environ.get("POSTGRES_USER")}:{os_environ.get("POSTGRES_PASSWORD")}@{os_environ.get("SQL_HOST")}:{os_environ.get("SQL_PORT")}/{os_environ.get("POSTGRES_TEST_DB", "TEST")}"


@pytest.fixture(name="session", autouse=True)
def session_fixture():
    if database_exists(TEST_DATABASE_URL):
        drop_database(TEST_DATABASE_URL)
    create_database(TEST_DATABASE_URL)
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    close_all_sessions()
    drop_database(TEST_DATABASE_URL)


@pytest.fixture(name="client")
def client_fixture(session: Session):  
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_user")
def mock_user(session):
    user = UserCreate(
        username="mock_user",
    )
    db_user = User.model_validate(user)
    session.add(db_user)
    db_user.is_admin = False
    db_user.auth_token = f"{db_user.username}::token"
    session.commit()
    session.refresh(db_user)
    return db_user


@pytest.fixture(name="mock_admin_user")
def mock_admin_user(session):
    admin = UserCreate(
        username="mock_admin",
    )
    db_user = User.model_validate(admin)
    session.add(db_user)
    db_user.is_admin = True
    db_user.auth_token = f"{db_user.username}::token"
    session.commit()
    session.refresh(db_user)
    return db_user
