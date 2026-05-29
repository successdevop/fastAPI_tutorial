from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.book.models import Book
from src.book.book_schema import BookUpdateModel, BookCreateModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        if not statement:
            raise HTTPException(detail="No books found, bookstore empty", status_code=status.HTTP_404_NOT_FOUND)

        output = await session.exec(statement)
        return output.all()

    async def get_a_book(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.bk_id == book_id)
        if not statement:
            raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)
        output = await session.exec(statement)
        return output.first()

    async def delete_a_book(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.bk_id == book_id)
        if not statement:
            raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(statement)
        await session.commit()
        return {"message":"Book deleted successfully"}

    async def update_a_book(self, book_id: str, book_data: BookUpdateModel, session: AsyncSession):
        book_to_update = self.get_a_book(book_id, session)
        if book_to_update is not None:
            book_to_dict = book_data.model_dump()

            for k, v in book_to_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()
        return book_to_update

    async def add_book(self, book_data: BookCreateModel, session: AsyncSession):
        new_book_dict = book_data.model_dump()

        new_book = Book(**new_book_dict)
        session.add(new_book)
        await session.commit()
        return new_book



