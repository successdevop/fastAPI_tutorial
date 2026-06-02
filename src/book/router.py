from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.book.book_service import BookService
from src.book.book_schema import BookUpdateModel, BookCreateModel, BookModel
from src.db.main import get_db_session
from src.auth.dependency import AccessTokenBearer


book_router = APIRouter()
core_service = BookService()
access_token_bearer = AccessTokenBearer()


@book_router.get("/", response_model=list[BookModel], status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_db_session), user_details=Depends(access_token_bearer)):
    return await core_service.get_all_books(session=session)


@book_router.get("/{book_id}", response_model=BookModel, status_code=status.HTTP_200_OK)
async def get_a_book(book_id: str, session: AsyncSession = Depends(get_db_session)):
    return await core_service.get_a_book(book_id, session=session)


@book_router.patch("/{book_id}", response_model=BookModel, status_code=status.HTTP_200_OK)
async def update_a_book(book_id: str, book_data: BookUpdateModel, session: AsyncSession = Depends(get_db_session)):
    return await core_service.update_a_book(book_id=book_id, book_data=book_data, session=session)


@book_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_a_book(book_id: str, session: AsyncSession = Depends(get_db_session)):
    return await core_service.delete_a_book(book_id, session=session)


@book_router.post("/", response_model=BookModel, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_db_session)):
    return await core_service.add_book(book_data=book_data, session=session)
