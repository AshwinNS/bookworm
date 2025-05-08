import pytest
from src.reviews.service import ReviewService
from src.reviews.schemas import ReviewCreateModel
from src.db.models import Book


async def test_check_book_exists_valid_book(async_session, book_data):
    # Arrange: Create a book in the database
    book = Book(**book_data)
    async_session.add(book)
    await async_session.commit()
    await async_session.refresh(book)

    # Act: Call the check_book_exists method
    review_service = ReviewService(session=async_session)
    retrieved_book = await review_service.check_book_exists(book.id)

    # Assert: Verify the book exists
    assert retrieved_book is not None
    assert retrieved_book.id == book.id
    assert retrieved_book.title == book.title


async def test_check_book_exists_invalid_book(async_session):
    # Arrange: Use a non-existent book ID
    non_existent_book_id = 9999

    # Act & Assert: Verify NotFoundError is raised
    review_service = ReviewService(session=async_session)
    with pytest.raises(Exception) as exc_info:
        await review_service.check_book_exists(non_existent_book_id)

    assert "Book with id 9999 not found" in str(exc_info.value)


async def test_get_all_book_reviews(async_session, book_data):
    # Arrange: Create a book in the database
    book = Book(**book_data)
    async_session.add(book)
    await async_session.commit()
    await async_session.refresh(book)

    # Act: Call the get_all_book_reviews method
    review_service = ReviewService(session=async_session)
    reviews = await review_service.get_all_book_reviews(book.id)

    # Assert: Verify the reviews are retrieved correctly
    assert reviews is not None
    assert len(reviews) == 0  # Assuming no reviews exist initially


async def test_add_book_review(async_session, book_data):
    # Arrange: Create a book in the database
    book = Book(**book_data)
    async_session.add(book)
    await async_session.commit()
    await async_session.refresh(book)

    # Create review data
    review_data = ReviewCreateModel(
        rating=5,
        review_text="Great book!",
        user_id=1
    )

    # Act: Call the add_book_review method
    review_service = ReviewService(session=async_session)
    created_review = await review_service.add_book_review(book.id, review_data)

    # Assert: Verify the review is created correctly
    assert created_review is not None
    assert created_review.rating == review_data.rating
    assert created_review.review_text == review_data.review_text