
from os import environ as os_environ

from fastapi import Depends
from sqlmodel import Session, select

from api.db import get_session
from api.models import Book
from llm import prompts
from llm.helper import OllamaClient


model_name = os_environ.get("MODEL_NAME", "llama3.2")
ollama_client = OllamaClient(model_name)

def generate_story(book_id: int, session: Session = Depends(get_session)):
    """Generate a random story."""
    query = "Generate a story based on {book.genre} genre. ignore genre and make the story if it doesn't make sense."
    response = ollama_client.chat(prompts.generate_story_prompt(), query)

    generated_story = response.get("response", "")  # Adjust this based on the actual response structure
    
    # with open("log.txt", mode="w") as email_file:
    #     content = f"notification for {book_id}: {generated_story}"
    #     email_file.write(content)

    db_book = session.exec(select(Book).where(Book.id == book_id)).first()
    if not db_book:
        raise ValueError(f"Book with ID {book_id} not found in the database.")
    db_book.story = generated_story

    # Save the updated book to the database
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
