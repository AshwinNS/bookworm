from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError

from src.db.models import User
from .schemas import UserCreateModel
from src.helper import NotFoundError


class UserService:
    """
    This class provides methods to create and read user
    """

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_users(self):
        """
        Get a list of all users

        Returns:
            list: list of users
        """
        try:
            statement = select(User)
            result = await self.session.exec(statement)
            return result.all()
        except Exception as e:
            raise NotFoundError("Users not found")


    async def create_user(self, user_create_data: UserCreateModel):
        """
        Create a new book

        Args:
            user_create_data (UserCreateModel): data to create a new user

        Returns:
            Book: the new book
        """
        try:
            new_user = User(**user_create_data.model_dump())

            self.session.add(new_user)
            new_user.auth_token = self.generate_auth_token(new_user.username)

            await self.session.commit()
            return new_user
        except Exception as e:
            raise NotFoundError("User already exists")


    async def get_token(self, username: str):
        """
        Get auth token of a given user

        Args:
            username (str): username to get token for

        Returns:
            Book: the new book
        """
        try:
            statement = select(User).where(User.username == username)
            db_user = await self.session.exec(statement)
            result = db_user.first()
            return result
        except Exception as e:
            raise NotFoundError("User not found")


    async def validate_token(self, username: str, token: str):
        """
        Validate the auth token of a given user

        Args:
            username (str): username to validate token for
            token (str): token to validate

        Returns:
            bool: True if the token is valid, False otherwise
        """
        statement = select(User).where(User.username == username).where(User.auth_token == token)
        db_user = await self.session.exec(statement).first()
        if db_user is None:
            raise NotFoundError("User not found")
        return db_user
    

    def generate_auth_token(self, username: str):
        """
        Generate a new auth token for the user

        Args:
            username (str): the username of the user

        Returns:
            str: the new auth token
        """
        return f"{username}::token"


    async def promote_to_admin(self, username: str):
        """
        Promotes a user to admin status.

        Args:
            username (str): The username of the user to be promoted.
        """
        try:
            # Query the user by username
            statement = select(User).where(User.username == username)
            result = await self.session.exec(statement)
            user = result.first()

            # Check if the user exists
            if not user:
                raise NotFoundError(f"User {username} not found")

            # Promote the user to admin
            user.is_admin = True
            await self.session.commit()
            return user

        except SQLAlchemyError as e:
            # Handle database-related errors
            raise RuntimeError(f"Database error occurred: {str(e)}")

        except Exception as e:
            # Handle any other unexpected errors
            raise RuntimeError(f"An unexpected error occurred: {str(e)}")
