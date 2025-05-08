# Book API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.main import get_session
from http import HTTPStatus
from .service import ReviewService
from .schemas import ReviewCreateModel, ReviewResponseModel
from src.helper import NotFoundError


review_router = APIRouter()

@review_router.get("/books/{book_id}/reviews/", status_code=HTTPStatus.OK, response_model=List[ReviewResponseModel])
async def get_book_reviews_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    """Get all reviews of a book"""
    try:
        book_reviews = await ReviewService(session).get_all_book_reviews(book_id)
        return book_reviews
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@review_router.post("/books/{book_id}/reviews/", status_code=HTTPStatus.CREATED)
async def add_new_book_review(
    book_id: int, review_create_data: ReviewCreateModel, session: AsyncSession = Depends(get_session)
):
    """Create a new review for a book"""
    try:
        book_review = await ReviewService(session).add_book_review(book_id, review_create_data)
        return book_review
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
