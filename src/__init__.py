from fastapi import FastAPI
from src.book.router import book_router


version = "v1"
app = FastAPI(
    title="Book app",
    description="A REST API for a book web service",
    version=version
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])