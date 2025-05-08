import pytest

from src.books.service import BookService
from src.books.schemas import BookCreateModel, BookUpdateModel


async def test_get_book_by_id(async_session, book_data):
    book_service = BookService(session=async_session)

    book_data = BookCreateModel(**book_data)
    created_book = await book_service.create_book(book_data)

    retrieved_book = await book_service.check_book_exists(created_book.id)

    assert retrieved_book is not None
    assert retrieved_book.id == created_book.id
    assert retrieved_book.title == created_book.title


async def test_create_book(async_session, book_data):
    # Pass the session to the service class
    book_service = BookService(session=async_session)

    # Create a new book
    book_data = BookCreateModel(**book_data)
    created_book = await book_service.create_book(book_data)

    # Assertions
    assert created_book.title == book_data.title
    assert created_book.author == book_data.author
    assert created_book.id is not None


async def test_get_all_books(async_session):
    book_service = BookService(session=async_session)
    book_data1 = BookCreateModel(title="Book 1", author="Author 1", year_published=2021, genre="Fiction")
    book_data2 = BookCreateModel(title="Book 2", author="Author 2", year_published=2022, genre="Non-Fiction")
    
    await book_service.create_book(book_data1)
    await book_service.create_book(book_data2)
    
    books = await book_service.get_all_books()
    
    assert len(books) >= 2
    assert any(book.title == "Book 1" for book in books)
    assert any(book.title == "Book 2" for book in books)


async def test_update_book(async_session, book_data):
    book_service = BookService(session=async_session)
    book_data = BookCreateModel(**book_data)
    created_book = await book_service.create_book(book_data)
    
    update_data = BookUpdateModel(title="New Title", author="New Author")
    updated_book = await book_service.update_book(created_book.id, update_data)
    
    assert updated_book.title == "New Title"
    assert updated_book.author == "New Author"


async def test_delete_book(async_session, book_data):
    book_service = BookService(session=async_session)
    book_data = BookCreateModel(**book_data)
    created_book = await book_service.create_book(book_data)
    
    delete_message = await book_service.delete_book(created_book.id)
    
    assert delete_message == f"Book with id {created_book.id} was successfully deleted"
    
    with pytest.raises(Exception):
        await book_service.check_book_exists(created_book.id)