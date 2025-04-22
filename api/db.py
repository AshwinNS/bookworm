from os import environ as os_environ
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = f"{os_environ.get("DB_ENGINE")}://{os_environ.get("POSTGRES_USER")}:{os_environ.get("POSTGRES_PASSWORD")}@{os_environ.get("SQL_HOST")}:{os_environ.get("SQL_PORT")}/{os_environ.get("POSTGRES_DB")}"
engine = create_engine(DATABASE_URL)


def init_db():
    """Create the database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session
