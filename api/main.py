from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import  Session

from api.db import init_db, get_session
from api.helper import init_app
from api.routers import books, reviews, assistant, user


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

@app.on_event('startup')
def on_startup():
    init_db()
    init_app()


app.include_router(router=books.routers, tags=["books"])
app.include_router(router=reviews.routers, tags=["reviews"])
app.include_router(router=assistant.routers, tags=["assistant"])
app.include_router(router=user.routers, tags=["user"])


@app.get("/health_check")
def main():
    """Health check endpoint."""
    return {"status": "Up and running!"}
