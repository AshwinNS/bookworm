
from http import HTTPStatus
from typing import Annotated
from redis import Redis
from sqlmodel import select
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlmodel.ext.asyncio.session import AsyncSession

from llm.helper import OllamaClient
from src.db.main import get_session
from src.db.models import User
from src.config import settings


api_key_header = APIKeyHeader(name="Authorization", 
                            description='Bearer token based auth system, token should be in "Bearer username::token" format',
                            auto_error=False)

class NotFoundError(Exception):
    """Exception raised when a any error occurred during CRUD."""
    pass

   
async def validate_auth_token(authorization: str = Security(api_key_header), session: AsyncSession = Depends(get_session)):
    """Authenticate a user."""
    if not authorization:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid Authorization header format.")
    if 'Bearer ' not in authorization:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid Authorization header format. Correct Format: 'Bearer <Token>'")
    
    token = authorization.strip().lower().replace("bearer ", "")
    try:
        # Assuming the format "username::token" in the Authorization header
        username, _ = token.split("::")
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token format. Expected 'username::token'")

    statement = select(User).where(User.username == username)
    db_user = await session.exec(statement)
    result = db_user.first()
    if result and result.auth_token == token:
        return result    
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token or user not found.")


def init_app():
    """Initialize the app."""
    ollama_client = OllamaClient(settings.MODEL_NAME)

    # If the model name is not set, raise an error and exit
    if ollama_client.model_name:
        try:
            ollama_client.is_model_available()
            return ollama_client
        except Exception as e:
            print(f"Model {ollama_client.model_name} is not available. Error: {e}")
            raise RuntimeError("Please pull the model using 'make pull-model' command.")


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
            redis_client = Redis(host=settings.REDIS_HOST,
                                port=settings.REDIS_PORT,
                                db=settings.REDIS_DB,
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