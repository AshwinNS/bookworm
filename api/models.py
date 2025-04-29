from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional, List
from pydantic import field_validator


# Book schema and pydantic models - Start
class BookBase(SQLModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None
    story: Optional[str] = Field(default=None)


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reviews: List["Review"] = Relationship(back_populates="book")

    __table_args__ = (UniqueConstraint("title", "author", name="uq_title_author"),)

class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None


class BookPublic(BookBase):
    id: int
    reviews: List["Review"] = []

# Review schema and pydantic models - Start
# Review schema and pydantic models - Start

class ReviewBase(SQLModel):
    user_id: int
    review_text: str
    rating: int

    @field_validator("rating")
    def validate_rating(cls, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating
    

class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")
    book: Book = Relationship(back_populates="reviews")


class ReviewCreate(ReviewBase):
    pass


class ReviewPublic(ReviewBase):
    id: int
    book_id: int
    # book: BookPublic

# Review schema and pydantic models - End

# User schema and pydantic models - Start

class UserBase(SQLModel):
    username: str

    @field_validator("username")
    def validate_username(cls, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_admin: bool = False
    auth_token: Optional[str] = None

    __table_args__ = (UniqueConstraint("username", name="uq_username"),)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    id: int
    auth_token: str

# User schema and pydantic models - End