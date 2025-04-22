from sqlmodel import SQLModel, Field
from typing import Optional


class Books(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    genre: str
    year_published: int
    summary: str
