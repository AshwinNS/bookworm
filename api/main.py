from typing import Annotated, List
from fastapi import Depends, FastAPI, Query

from .db import init_db, get_session
from sqlmodel import select, Session
from .models import Books

app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event('startup')
def on_startup():
    init_db()


@app.get("/")
def main():
    return {"status": "Up and running!"}

# endpoints for books - Start

@app.get("/books/", response_model=List[Books])
async def get_books(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    """
    Fetch a list of books from the database with optional pagination.
    Args:
        session (SessionDep): The database session dependency used to execute queries.
        offset (int, optional): The number of records to skip before starting to fetch. Defaults to 0.
        limit (Annotated[int, Query(le=100)], optional): The maximum number of records to fetch, 
            constrained to a maximum value of 100. Defaults to 100.
    Returns:
        List[Books]: A list of book records retrieved from the database.
    """
    
    heroes = session.exec(select(Books).offset(offset).limit(limit)).all()
    return heroes


@app.post("/books/")
def create_book(book: Books, session: SessionDep) -> Books:
    """
    Creates a new book record in the database.
    Args:
        book (Books): The book object to be added to the database.
        session (SessionDep): The database session used to perform the operation.
    Returns:
        Books: The newly created and refreshed book object.
    """
    
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

# endpoints for books - End