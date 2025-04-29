from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, Session

from api.db import get_session
from api.helper import validate_auth_token
from api.models import User, UserCreate, UserPublic

routers = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@routers.get("/validate_token", response_model=str)
def validate_token(current_user: str = Depends(validate_auth_token)):
    """
    Validate the auth token.
    """
    return f"{current_user.username}, Your token is valid."


@routers.get("/users", response_model=List[User])
def get_users(session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(100, le=100)) -> List[User]:
    """
    Get list of users with pagination.
    """
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users


@routers.post("/user", response_model=UserPublic)
def create_user(user: UserCreate,session: SessionDep) -> User:
    """
    Create new user.
    """
    try:
        db_user = User.model_validate(user)
        session.add(db_user)
        db_user.auth_token = db_user.username + "::token"  # Example token generation
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="User already exists.")


@routers.get("/get_token/{username}", response_model=UserPublic)
def get_token(username: str, session: SessionDep) -> User:
    """
    Get the auth token for a user.
    This method should not be exposed with basic auth.
    """
    statement = select(User).where(User.username == username)
    db_user = session.exec(statement).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user
