from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.books.routes import book_router
from src.reviews.routes import review_router
from src.users.routes import user_router
from src.assistant.routes import assistant_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is shutting down")


app = FastAPI(
    title="Book service",
    version="0.1.0",
    description="A simple web service for a book application",
    lifespan=lifespan,
)

@app.router.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(book_router, tags=["books"])
app.include_router(review_router, tags=["reviews"])
app.include_router(user_router, tags=["users"])
app.include_router(assistant_router, tags=["assistant"])
