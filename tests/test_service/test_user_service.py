import pytest

from src.users.service import UserService
from src.users.schemas import UserCreateModel
from src.db.models import User
from src.helper import NotFoundError


async def test_get_all_users_success(async_session, mock_user, mock_admin_user):
    user_service = UserService(async_session)
    users = await user_service.get_all_users()

    # Assert
    assert len(users) > 0
    assert isinstance(users[0], User)


async def test_create_user_success(async_session):
    admin = UserCreateModel(
        username="mock_admin",
    )
    user_service = UserService(async_session)
    db_user = await user_service.create_user(admin)
    assert isinstance(db_user, User)
    assert db_user.username == "mock_admin"
    assert db_user.auth_token is not None
    assert db_user.is_admin is False


async def test_promote_to_admin_success(async_session, mock_user):
    
    user_service = UserService(async_session)
    promoted_user = await user_service.promote_to_admin(mock_user.username)

    # Assert
    assert promoted_user.is_admin is True


async def test_get_token_success(async_session, mock_user):
    user_service = UserService(async_session)
    user_obj = await user_service.get_token(mock_user.username)

    # Assert
    assert user_obj.auth_token is not None
    assert user_obj.auth_token == "mock_user::token"
