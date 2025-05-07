import pytest
import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.testclient import TestClient

from src.db.main import get_session
from src import app
from src.config import settings
from src.users.schemas import UserCreateModel
from src.users.service import UserService

async_engine = create_async_engine(url=str(settings.ASYNC_TEST_DATABASE_URI), echo=True)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def connection():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        try:
            yield conn
        finally:
            await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture()
async def async_session(connection: AsyncConnection):
    async with AsyncSession(connection, expire_on_commit=False) as async_session_:
        yield async_session_


@pytest_asyncio.fixture(autouse=True)
async def override_dependency(async_session: AsyncSession):
    app.dependency_overrides[get_session] = lambda: async_session


@pytest_asyncio.fixture()
def client_fixture(async_session: Session):  
    def get_session_override():
        return async_session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def book_data():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "genre": "Fiction",
        "year_published": 2023,
    }


@pytest_asyncio.fixture(name="mock_admin_user")
async def mock_admin_user(async_session):
    admin = UserCreateModel(
        username="mock_admin",
    )
    user_service = UserService(async_session)
    db_user = await user_service.create_user(admin)
    await user_service.promote_to_admin(db_user.username)
    return db_user


@pytest_asyncio.fixture(name="mock_user")
async def mock_user(async_session):
    admin = UserCreateModel(
        username="mock_user",
    )
    user_service = UserService(async_session)
    db_user = await user_service.create_user(admin)
    return db_user
