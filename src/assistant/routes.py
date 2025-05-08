# Assistant API endpoints

from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from llm import prompts
from llm.helper import OllamaClient
from src.db.models import Book, Review
from src.helper import NotFoundError, init_app
from src.db.main import get_session
from src.helper import RedisClient


assistant_router = APIRouter()
redis = RedisClient().get_client()
SessionDep = Annotated[AsyncSession, Depends(get_session)]
Client = Annotated[OllamaClient, Depends(init_app)]


@assistant_router.post("/assistant/")
async def assistant(q: str, ollama_client: Client):
    """
    Handles the assistant functionality by processing a query and returning a response.
    """
    try:
        response = await ollama_client.chat(prompts.assistant_prompt(), q)
        return response
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@assistant_router.post("/books/{book_id}/summary")
async def generate_summary(book_id: int, ollama_client: Client, session: SessionDep):
    """
    Generate a summary for a book based on its reviews.
    """
    statement = select(Book).where(Book.id == book_id)
    result = await session.exec(statement)
    db_book = result.first()
    if not db_book:
        raise NotFoundError(f"Book with id {book_id} not found")

    reviews_statement = select(Review).where(Review.book_id == book_id)
    res = await session.exec(reviews_statement)
    reviews = res.all()
    response = await ollama_client.chat(prompts.generate_summary_prompt(reviews, db_book), '')
    if not response:
        raise HTTPException(status_code=500, detail="Failed to generate summary")
    # # Update the book with the generated summary
    summary = response.get("response", "")
    if summary.startswith("Summary:"):
        summary = summary.split("Summary:")[1].strip()
    db_book.summary = summary
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    
    return response



@assistant_router.get("/recommendations/")
async def get_recommendations(session: SessionDep, ollama_client: Client):
    """
    Generate book recommendations based on user watch history and available books in the database.
    Notes:
        - The function retrieves all books from the database and formats them into a string.
        - It checks if Redis is available to fetch the user's watch history.
        - If Redis is available, it constructs a watch history string and sends it along with the book dataset
          to the recommendation service.
        - If Redis is not available, it logs a message indicating the unavailability of Redis.
    """
    statement = select(Book)
    result = await session.exec(statement)
    books = result.all()
    if not books:
        raise NotFoundError(f"Error while getting books from database")

    books_str = str()
    for book in books:
        books_str += f"{book.title} of genre {book.genre}, "

    if redis.ping():
        user_watch_history = redis.hgetall('book_title:watch')
        watch_history_string = str()
        for book, watch_count in user_watch_history.items():
            book_title, genre = book.split('::')
            watch_history_string += f"{book_title} for genre {genre} was watched {watch_count} times, "
        response = await ollama_client.chat(prompts.recommendations_prompt(),
                                    f'I have read/watched {watch_history_string}, recommend me books from this dataset {books_str}')
    else:
        print("Redis is not available.")
        response = {"error": "Redis is unavailable. Recommendations cannot be fetched."}
        
    if not response:
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations")
    return response
