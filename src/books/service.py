from typing import Annotated
from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.db.main import get_session
from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel
from src.helper import NotFoundError


class BookService:
    """
    This class provides methods to create, read, update, and delete books
    """

    def __init__(self, session: AsyncSession):
        self.session = session


    async def check_book_exists(self, book_id: int):
        """
        Check if a book exists in the database

        Args:
            book_id (str): the id of the book
        """
        try:
            statement = select(Book).where(Book.id == book_id)
            result = await self.session.exec(statement)
            book_data = result.first()
            if not book_data:
                raise NotFoundError(f"Book with id {book_id} not found")
            return book_data
        except Exception as e:
            raise NotFoundError(f"Book not found", str(e))
        

    async def get_all_books(self):
        """
        Get a list of all books

        Returns:
            list: list of books
        """
        try:
            statement = select(Book)
            result = await self.session.exec(statement)
            return result.all()
        except Exception as e:
            raise NotFoundError(f"Books not found")


    async def create_book(self, book_create_data: BookCreateModel):
        """
        Create a new book

        Args:
            book_create_data (BookCreateModel): data to create a new

        Returns:
            Book: the new book
        """
        try:
            new_book = Book(**book_create_data.model_dump())
            self.session.add(new_book)
            await self.session.commit()
            return new_book
        except Exception:
            raise NotFoundError(f"Book not created")


    async def get_book_with_id(self, book_id: int):
        """Get a book by its id.

        Args:
            book_id (str): the id of the book

        Returns:
            Book: the book object
        """
        book = await self.check_book_exists(book_id)
        return book



    async def update_book(self, book_id: int, book_update_data: BookUpdateModel):
        """
        Updates an existing book in the database with the provided data.
        Args:
            book_id (str): The unique identifier of the book to be updated.
            book_update_data (BookUpdateModel): An instance containing the updated book data.
        Returns:
            Book: The updated book object.
        """
        
        book = await self.check_book_exists(book_id)

        try:
            for key, value in book_update_data.model_dump(exclude_none=True).items():
                setattr(book, key, value)

            await self.session.commit()
            return book
        except Exception:
            raise NotFoundError(f"Book not updated")


    async def delete_book(self, book_id: int):
        """
        Deletes a book from the database based on the provided unique identifier (id).
        Args:
            book_id (str): The unique identifier of the book to be deleted.
        Returns:
            None
        """
        book = await self.check_book_exists(book_id)

        try:
            await self.session.delete(book)
            await self.session.commit()
            return f"Book with id {book_id} was successfully deleted"
        except Exception:
            raise NotFoundError(f"Book not deleted")
