from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session

from api.db import get_session
from api.models import *

routers = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@routers.get("/books/{book_id}/reviews/", response_model=List[ReviewPublic])
def get_reviews(book_id: int, session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    """
    Retrieve a list of reviews for a specific book.
    Args:
        book_id (int): The ID of the book for which reviews are being retrieved.
        offset (int, optional): The number of reviews to skip before starting to collect the result set. Defaults to 0.
        limit (Annotated[int, Query(le=100)], optional): The maximum number of reviews to return, with a maximum value of 100. Defaults to 100.
    Returns:
        List[Review]: A list of reviews associated with the specified book.
    Raises:
        HTTPException: If the book with the given ID is not found, raises a 404 error with the message "Book not found".
    """
    
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews = session.exec(select(Review).where(Review.book_id == book_id).offset(offset).limit(limit)).all()
    return reviews


@routers.post("/books/{book_id}/reviews/", response_model=ReviewPublic)
def create_or_update_review(book_id: int, review: ReviewCreate, session: SessionDep) -> Review:
    """
    Create or update a review for a specific book.
    If a review by the same user for the given book already exists, it updates the review.
    Otherwise, it creates a new review.
    Args:
        book_id (int): The ID of the book for which the review is being created or updated.
        review (ReviewCreate): The review data provided by the user.
    Returns:
        Review: The created or updated review object.
    Raises:
        HTTPException: If the book with the given ID is not found in the database.
    """

    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if the user has already provided a review for this book
    # Assuming a user can add only one review per book
    existing_review = session.exec(
        select(Review).where(Review.book_id == book_id, Review.user_id == review.user_id)
    ).first()
    
    if existing_review:
        # Update the existing review
        review_data = review.model_dump(exclude_unset=True)
        for key, value in review_data.items():
            setattr(existing_review, key, value)
        session.commit()
        session.refresh(existing_review)
        return existing_review
    else:
        # Create a new review
        db_review = Review.model_validate(review)
        db_review.book_id = book_id
        session.add(db_review)
        session.commit()
        session.refresh(db_review)
        return db_review
