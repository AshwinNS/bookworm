from os import environ as os_environ
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from api.db import get_session
from api.models import Book
from llm import prompts
from llm.helper import OllamaClient

routers = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

# Check if the model name is set in the environment variables
model_name = os_environ.get("MODEL_NAME", "llama3.2")
ollama_client = OllamaClient(model_name)

# If the model name is not set, raise an error and exit
if ollama_client.model_name:
    try:
        ollama_client.is_model_available()
    except Exception as e:
        print(f"Model {ollama_client.model_name} is not available. Error: {e}")
        raise RuntimeError("Please pull the model using 'make pull-model' command.")


@routers.post("/assistant/")
def assistant(q: str, session: SessionDep):
    response = ollama_client.chat(prompts.assistant_prompt(), q)
    return response


@routers.post("/books/{book_id}/summary")
def generate_summary(book_id: int, session: SessionDep):
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
