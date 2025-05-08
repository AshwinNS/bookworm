from sqlmodel import SQLModel
from pydantic import field_validator


class UserBase(SQLModel):
    username: str
    # is_admin: bool = False # Uncomment if you want to include is_admin in the base model

    @field_validator("username")
    def validate_username(cls, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username


class UserCreateModel(UserBase):
    pass


class UserResponseModel(UserBase):
    id: int
    auth_token: str
