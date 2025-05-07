# Book API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.main import get_session
from http import HTTPStatus
from .service import UserService
from .schemas import UserCreateModel, UserResponseModel
from src.helper import NotFoundError, validate_auth_token

user_router = APIRouter()

@user_router.get("/validate_token", response_model=str)
async def validate_token(current_user: str = Depends(validate_auth_token)):
    """validate token"""
    return f"{current_user.username}, Your token is valid."
    

@user_router.post("/users", response_model=UserResponseModel)
async def create_users(
    user_create_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    """Create a new user"""
    try:
        book_review = await UserService(session).create_user(user_create_data)
        return book_review
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@user_router.get("/users", response_model=List[UserResponseModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    """Get all users"""
    try:
        users = await UserService(session).get_all_users()
        return users
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    

@user_router.get("/get_token/{username}", response_model=UserResponseModel)
async def get_token(
    username: str, session: AsyncSession = Depends(get_session)
):
    """Get auth token of a given user"""
    try:
        user = await UserService(session).get_token(username)
        return user
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@user_router.post("/promote_to_admin/{username}", response_model=UserResponseModel)
async def promote_to_admin(username: str, session: AsyncSession = Depends(get_session), current_user: str = Depends(validate_auth_token)):
    """Promote a user to admin (Require admin user to access this endpoint)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You do not have permission to promote this user.")
    
    try:
        user = await UserService(session).promote_to_admin(username)
        return user
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
