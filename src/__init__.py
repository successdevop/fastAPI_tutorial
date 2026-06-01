from fastapi import FastAPI
from src.book.router import book_router
from src.auth.user_routes import user_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("Server has been stopped")


version = "v1"
app = FastAPI(
    title="Book app",
    description="A REST API for a book web service",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(user_router, prefix=f"/api/{version}/auth", tags=["auth"])