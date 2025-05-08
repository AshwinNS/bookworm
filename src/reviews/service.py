from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Review, Book
from .schemas import ReviewCreateModel
from sqlmodel import select
from src.helper import NotFoundError


class ReviewService:
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

        Returns:
            bool: True if the book exists, False otherwise
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


    async def get_all_book_reviews(self, book_id: int):
        """
        Get a list of all reviews

        Returns:
            list: list of reviews
        """
        await self.check_book_exists(book_id)

        try:
            reviews_statement = select(Review).where(Review.book_id == book_id)
            reviews = await self.session.exec(reviews_statement)
            return reviews.all()
        except Exception:
            raise NotFoundError(f"Reviews not found for book {book_id}")

    async def add_book_review(self, book_id: int, review_create_data: ReviewCreateModel):
        """
        Create a new book review

        Args:
            review_create_data (ReviewCreateModel): data to create a new review

        Returns:
            Book: the new review
        """
        await self.check_book_exists(book_id)
        
        get_review_statement = select(Review).where(Review.book_id == book_id).where(Review.user_id == review_create_data.user_id)
        existing_review_obj = await self.session.exec(get_review_statement)
        existing_review = existing_review_obj.first()

        if existing_review:
            try:
                review_data = review_create_data.model_dump()
                for key, value in review_data.items():
                    setattr(existing_review, key, value)
                await self.session.commit()
                return existing_review
            except Exception as e:
                raise NotFoundError("Review not updated")
        else:
            try:
                new_review = Review(**review_create_data.model_dump())
                new_review.book_id = book_id
                self.session.add(new_review)
                await self.session.commit()
                return new_review
            except Exception:
                raise NotFoundError("Review not created")
