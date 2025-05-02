from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.db import get_session
from api.helper import RedisClient, init_app
from api.models import Book
from llm import prompts
from llm.helper import OllamaClient

routers = APIRouter()
redis = RedisClient().get_client()
SessionDep = Annotated[Session, Depends(get_session)]
Client = Annotated[OllamaClient, Depends(init_app)]


@routers.post("/books/{book_id}/summary")
def generate_summary(book_id: int, session: SessionDep, ollama_client: Client):
    """
    Generate a summary for a book based on its reviews.
    """
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    reviews = db_book.reviews
    response = ollama_client.chat(prompts.generate_summary_prompt(reviews, db_book), '')
    if not response:
        raise HTTPException(status_code=500, detail="Failed to generate summary")
    # Update the book with the generated summary
    summary = response.get("response", "")
    if summary.startswith("Summary:"):
        summary = summary.split("Summary:")[1].strip()
    db_book.summary = summary
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    
    return response


@routers.get("/recommendations/")
def get_recommendations(session: SessionDep, ollama_client: Client):
    """
    Generate book recommendations based on user watch history and available books in the database.
    Notes:
        - The function retrieves all books from the database and formats them into a string.
        - It checks if Redis is available to fetch the user's watch history.
        - If Redis is available, it constructs a watch history string and sends it along with the book dataset
          to the recommendation service.
        - If Redis is not available, it logs a message indicating the unavailability of Redis.
    """
    books = session.exec(select(Book)).all()
    books_str = str()
    for book in books:
        db_books = Book.model_validate(book)
        books_str += f"{db_books.title} of genre {db_books.genre}, "
    if redis.ping():
        user_watch_history = redis.hgetall('book_title:watch')
        watch_history_string = str()
        for book, watch_count in user_watch_history.items():
            book_title, genre = book.split('::')
            watch_history_string += f"{book_title} for genre {genre} was watched {watch_count} times, "
        response = ollama_client.chat(prompts.recommendations_prompt(),
                                    f'I have read/watched {watch_history_string}, recommend me books from this dataset {books_str}')
    else:
        print("Redis is not available.")
        
    if not response:
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations")
    return response
