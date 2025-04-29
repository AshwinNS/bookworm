from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, Session

from api.db import get_session
from api.models import Book, BookCreate, BookPublic, BookUpdate
from api.helper import generate_story, validate_auth_token

routers = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@routers.get("/books/", response_model=List[BookPublic])
async def get_books(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    """
    Fetch list of books from the database with optional pagination.
    Args:
        session (SessionDep): The database session dependency used to execute queries.
        offset (int, optional): The number of records to skip before starting to fetch. Defaults to 0.
        limit (int, optional): The maximum number of records to fetch. Must be less than or equal to 100. Defaults to 100.
    Returns:
        List[Book]: A list of Book objects retrieved from the database.
    """
    heroes = session.exec(select(Book).offset(offset).limit(limit)).all()
    return heroes


@routers.post("/books/", response_model=BookPublic)
def create_book(book: BookCreate, session: SessionDep, background_tasks: BackgroundTasks) -> Book:
    """
    Creates a new book record in the database.
    Args:
        book (BookCreate): The data required to create a new book, validated against the BookCreate schema.
    Returns:
        Book: The newly created book record after being added to the database.
    """
    try:
        db_books = Book.model_validate(book)
        session.add(db_books)
        session.commit()
        session.refresh(db_books)
    
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="A book with the same title and author already exists.")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating book: {str(e)}")
    
    # Add the book creation task to the background tasks
    background_tasks.add_task(generate_story, db_books.id, session)
    return db_books


@routers.get("/books/{book_id}", response_model=BookPublic)
def get_book_by_id(book_id: int, session: SessionDep) -> Book:
    """
    Retrieve a book from the database by its ID.
    Args:
        book_id (int): The unique identifier of the book to retrieve.
    Returns:
        Book: The book object corresponding to the given ID.
    Raises:
        HTTPException: If no book with the given ID is found, raises a 404 error with the message "Book not found".
    """
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@routers.put("/books/{book_id}", response_model=BookPublic)
def update_book(book_id: int, book: BookUpdate, session: SessionDep, current_user: str = Depends(validate_auth_token)) -> Book:
    """
    Update an existing book in the database.
    Args:
        book_id (int): The ID of the book to update.
        book (BookUpdate): An object containing the updated book data.
    Returns:
        Book: The updated book object.
    Raises:
        HTTPException: If the book with the given ID is not found (404).
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to update this book.")
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update only the fields provided in the request
    try:
        book_data = book.model_dump(exclude_unset=True)
        for key, value in book_data.items():
            setattr(db_book, key, value)
        session.commit()
        session.refresh(db_book)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating book: {str(e)}")
    
    return db_book


@routers.delete("/books/{book_id}", response_model=str)
def delete_book(book_id: int, session: SessionDep, current_user: str = Depends(validate_auth_token)) -> str:
    """
    Deletes a book from the database based on the provided book ID.
    Args:
        book_id (int): The ID of the book to be deleted.
    Returns:
        str: A success message indicating the book has been deleted.
    Raises:
        HTTPException: If the book with the given ID is not found, raises a 404 error.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this book.")
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    session.delete(db_book)
    session.commit()
    return f"Book with ID {book_id} has been deleted successfully."
