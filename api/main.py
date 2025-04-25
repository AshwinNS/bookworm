from os import environ as os_environ
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import  Session

from api.db import init_db, get_session
from llm.helper import OllamaClient
from llm import prompts
from api.routers import books, reviews


app = FastAPI(
    title="Bookworm API",
    description="""### Bookworm API helps you do awesome stuff with books and reviews. 🚀""",
    openapi_tags=[
        {
            "name": "books",
            "description": "Books API to help interact with Books db.",
        },
        {
            "name": "reviews",
            "description": "Reviews API to help interact with Reviews db.",
        },
        {
            "name": "assistant",
            "description": "LLM assistant operations.",
        },
    ]
)
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

app.include_router(router=books.routers)
app.include_router(router=reviews.routers)


@app.on_event('startup')
def on_startup():
    init_db()


@app.get("/health_check")
def main():
    """Health check endpoint."""
    return {"status": "Up and running!"}


@app.post("/assistant/", tags=["assistant"])
def generate_summary(q: str, session: SessionDep):
    response = ollama_client.chat(prompts.assistant_prompt(), q)
    return response
