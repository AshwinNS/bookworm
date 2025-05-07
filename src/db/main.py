from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings
from sqlalchemy.orm import declarative_base

Base = declarative_base()
target_metadata = Base.metadata
async_engine = create_async_engine(url=str(settings.ASYNC_DATABASE_URI), echo=True)
async_test_engine = create_async_engine(url=str(settings.ASYNC_TEST_DATABASE_URI), echo=True)


async def init_db():
    """Create the database tables"""
    async with async_engine.begin() as conn:
        
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
