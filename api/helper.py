from json import load as json_load
from os import environ as os_environ, path as os_path
from fastapi import Depends, HTTPException, Security
from sqlmodel import Session, select
from fastapi.security.api_key import APIKeyHeader
from redis import Redis
from redis.exceptions import ConnectionError

from api.db import get_session
from api.models import Book, User
from llm import prompts
from llm.helper import OllamaClient

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
model_name = os_environ.get("MODEL_NAME", "llama3.2")
ollama_client = OllamaClient(model_name)

class RedisClient:
    """Redis client class."""

    def __init__(self):
        self.redis = None

    def get_client(self):
        if not self.redis:
            self.redis = self.get_redis()
        return self.redis
    
    def get_redis(self):
        """Get the Redis client."""
        try:
            redis_client = Redis(host=os_environ.get("REDIS_HOST", "redis"),
                                port=int(os_environ.get("REDIS_PORT", 6379)),
                                db=int(os_environ.get("REDIS_DB", 0)),
                                password=os_environ.get("REDIS_PASSWORD", None),
                                decode_responses=True)
            redis_client.ping()
            return redis_client
        except ConnectionError as e:
            print(f"Redis connection error: {e}")
            raise RuntimeError("Redis server is not reachable.")
    
    def ping(self):
        """Ping the Redis server."""
        try:
            self.redis.ping()
            return True
        except ConnectionError as e:
            print(f"Redis connection error: {e}")
            return False


def generate_story(book_id: int, session: Session = Depends(get_session)):
    """Generate a random story."""
    db_book = session.exec(select(Book).where(Book.id == book_id)).first()
    if not db_book:
        raise ValueError(f"Book with ID {book_id} not found in the database.")
    
    query = f"Generate a story based on {db_book.genre} genre. ignore genre and make the story if it doesn't make sense."
    response = ollama_client.chat(prompts.generate_story_prompt(), query)

    generated_story = response.get("response", "")  # Adjust this based on the actual response structure

    db_book.story = generated_story

    # Save the updated book to the database
    session.add(db_book)
    session.commit()
    session.refresh(db_book)


def verify_token(username: str, token: str, session: Session):
    db_user = session.exec(select(User).where(User.username == username)).first()
    if db_user and db_user.auth_token == token:
        return True
    return False


def validate_auth_token(authorization: str = Security(api_key_header), session: Session = Depends(get_session)):
    """Authenticate a user."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format.")
    if 'Bearer ' not in authorization:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format. Correct Format: 'Bearer <Token>'")
    
    token = authorization.strip().lower().replace("bearer ", "")
    try:
        # Assuming the format "username::token" in the Authorization header
        username, _ = token.split("::")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format. Expected 'username::token'")

    db_user = session.exec(select(User).where(User.username == username)).first()
    if db_user and db_user.auth_token == token:
        return db_user    
    raise HTTPException(status_code=401, detail="Invalid token or user not found.")


def init_app():
    """Initialize the app."""
    # Check if the model name is set in the environment variables
    model_name = os_environ.get("MODEL_NAME", "llama3.2")
    ollama_client = OllamaClient(model_name)

    # If the model name is not set, raise an error and exit
    if ollama_client.model_name:
        try:
            ollama_client.is_model_available()
            return ollama_client
        except Exception as e:
            print(f"Model {ollama_client.model_name} is not available. Error: {e}")
            raise RuntimeError("Please pull the model using 'make pull-model' command.")
