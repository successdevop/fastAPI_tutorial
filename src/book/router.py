from typing import List

from fastapi import APIRouter

from src.book.core import Core
from src.book.book_schema import BookModel, BookUpdateModel


book_router = APIRouter()
core_service = Core()


@book_router.get("/", response_model=List)
async def get_all_books():
    return core_service.get_all_books()


@book_router.get("/")
async def get_a_book(book_id: int):
    return core_service.get_a_book(book_id)


@book_router.patch("/")
async def update_a_book(book_id: int, book_data: BookUpdateModel):
    return core_service.update_a_book(book_id=book_id, book_data=book_data)


@book_router.delete("/")
async def delete_a_book(book_id: int):
    return core_service.delete_a_book(book_id)


@book_router.post("/")
async def create_book(book_data: BookModel):
    return core_service.add_book(book_data=book_data)