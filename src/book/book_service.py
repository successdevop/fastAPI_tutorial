from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.book.models import Book
from src.book.book_schema import BookUpdateModel, BookCreateModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        output = await session.execute(statement)
        books = output.scalars().all()

        if not books:
            raise HTTPException(detail="No books found, bookstore empty", status_code=status.HTTP_404_NOT_FOUND)
        return books

    async def get_a_book(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.bk_id == book_id)
        output = await session.execute(statement)
        book =  output.one_or_none()

        if not book:
            raise HTTPException(detail=f"Book with id {book_id} not found", status_code=status.HTTP_404_NOT_FOUND)
        return book

    async def delete_a_book(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.bk_id == book_id)
        output = await session.execute(statement)
        book = output.one_or_none()

        if not book:
            raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(statement)
        await session.commit()
        return {"message":f"Book with id {book_id} deleted successfully"}

    async def update_a_book(self, book_id: str, book_data: BookUpdateModel, session: AsyncSession):
        book_to_update = self.get_a_book(book_id, session)
        if book_to_update is not None:
            book_to_dict = book_data.model_dump(exclude_unset=True)

            for k, v in book_to_dict.items():
                setattr(book_to_update, k, v)

            session.add(book_to_update)
            await session.commit()
            await session.refresh(book_to_update)
        return book_to_update

    async def add_book(self, book_data: BookCreateModel, session: AsyncSession):
        new_book_dict = book_data.model_dump()
        new_book = Book(**new_book_dict)

        statement = select(Book).where(Book.bk_id == new_book.bk_id)
        result = await session.execute(statement)
        book = result.one_or_none()

        if book:
            raise HTTPException(detail=f"Book with id {new_book.bk_id} already exists",
                                status_code=status.HTTP_409_CONFLICT)

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book



