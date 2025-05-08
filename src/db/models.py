from typing import List, Optional
from pydantic import field_validator
from sqlmodel import  Field, Relationship, UniqueConstraint

from src.reviews.schemas import ReviewBase
from src.books.schemas import BookBase
from src.users.schemas import UserBase

class Book(BookBase, table = True):
    """
    This class represents a book in the database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    reviews: List["Review"] = Relationship(back_populates="book")
    __table_args__ = (UniqueConstraint("title", "author", name="uq_title_author"),)

    def __repr__(self) -> str:
        return f"Book => {self.title}"


class Review(ReviewBase, table = True):
    """
    This class represents a book in the database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")
    book: Book = Relationship(back_populates="reviews")

    @field_validator("rating")
    def validate_rating(cls, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating


class User(UserBase, table = True):
    """
    This class represents a user in the database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    is_admin: bool = False
    auth_token: Optional[str] = None

    __table_args__ = (UniqueConstraint("username", name="uq_username"),)
