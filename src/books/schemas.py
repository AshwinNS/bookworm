from typing import Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel


class BookBase(SQLModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None
    story: Optional[str] = Field(default=None)


class BookResponseModel(BookBase):
    """
        This class is used to validate the response when getting book objects
    """
    id: int


class BookCreateModel(BaseModel):
    """
        This class is used to validate the request when creating book
    """
    title: str
    author: str
    genre: str
    year_published: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Cookbook",
                "author": "John Doe",
                "genre": "Programming",
                "year_published": 2025,
            }
        }
    }


class BookUpdateModel(SQLModel):
    """
        This class is used to validate the request when updating a book
    """
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None
    story: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Cookbook",
                "author": "John Doe",
                "genre": "Programming",
                "year_published": 2025,
                "summary": "A comprehensive gide to Python programming.",
                "story": "This book covers advanced Python programming techniques."
            }
        }
    }
