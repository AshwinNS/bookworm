# Book API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.helper import RedisClient
from src.db.main import get_session
from http import HTTPStatus
from .service import BookService
from .schemas import BookCreateModel, BookResponseModel, BookUpdateModel
from src.helper import NotFoundError, validate_auth_token

book_router = APIRouter(prefix="/books")
redis = RedisClient().get_client()


@book_router.get("/", status_code=HTTPStatus.OK, response_model=List[BookResponseModel])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    """Get all books"""
    try:
        books = await BookService(session).get_all_books()
        return books
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@book_router.post("/", status_code=HTTPStatus.CREATED)
async def create_book(
    book_create_data: BookCreateModel, session: AsyncSession = Depends(get_session)
):
    """Create a new book"""
    try:
        new_book = await BookService(session).create_book(book_create_data)
        return new_book
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@book_router.get("/{book_id}", status_code=HTTPStatus.OK)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    """Get a book by its id"""
    try:
        book = await BookService(session).get_book_with_id(book_id)

        # update the redis cache when user checkout any book
        if redis.ping():
            watch_key = 'book_title:watch'
            title = book.title
            genre = book.genre
            field_key = f"{title}::{genre}"
            watched = redis.hmget(watch_key, [field_key])
            if watched:
                redis.hincrby(watch_key, field_key, 1)
            else:
                redis.hset(watch_key, field_key, 1)

        return book
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@book_router.put("/{book_id}", status_code=HTTPStatus.OK)
async def update_book(
                book_id: int,
                update_data: BookUpdateModel,
                session: AsyncSession = Depends(get_session),
                current_user: str = Depends(validate_auth_token)
            ):
    """Update a book by its id"""
    if not current_user.is_admin:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You do not have permission to update this book.")
    
    try:
        await BookService(session).get_book(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    try:
        updated_book = await BookService(session).update_book(book_id, update_data)
        return updated_book
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@book_router.delete("/{book_id}", status_code=HTTPStatus.OK, response_model=str)
async def delete_book(book_id: int,
                session: AsyncSession = Depends(get_session),
                current_user: str = Depends(validate_auth_token)
            ):
    """Delete a book"""
    if not current_user.is_admin:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You do not have permission to delete this book.")

    try:
        result = await BookService(session).delete_book(book_id)
        return result
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
