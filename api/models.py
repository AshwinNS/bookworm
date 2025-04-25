from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import field_validator


# Book schema and pydantic models - Start
class BookBase(SQLModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

    @field_validator("summary", mode="before")
    def validate_summary(cls, data):
        if not data:
            return "No summary available."
        return data


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reviews: List["Review"] = Relationship(back_populates="book")


class BookCreate(BookBase):
    pass


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
