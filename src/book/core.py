from typing import List
from fastapi import status
from fastapi.exceptions import HTTPException

from src.book.book_schema import BookUpdateModel, BookModel
from src.book.data import data


class Core:
    def __init__(self):
        self.data = data

    def get_all_books(self) -> List:
        return self.data

    def get_a_book(self, book_id: int) -> dict:
        for book in self.data:
            if book.get("id") == book_id:
                return book
        raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete_a_book(self, book_id: int):
        for book in self.data:
            if book.get("id") == book_id:
                self.data.remove(book)
                return {"message":"Book deleted"}
        raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)

    def update_a_book(self, book_id: int, book_data: BookUpdateModel) -> dict:
        for book in self.data:
            if book.get("id") == book_id:
                if book_data.title is not None:
                    book["title"] = book_data.title
                if book_data.publisher is not None:
                    book["publisher"] = book_data.publisher
                if book_data.page_count is not None:
                    book["page_count"] = book_data.page_count
                if book_data.language is not None:
                    book["language"] = book_data.language
                return book
        raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)

    def add_book(self, book_data: BookModel):
        new_book = book_data.model_dump()

        if any(bk["id"] == new_book["id"] for bk in self.data):
            raise HTTPException(detail=f"Book with id {new_book['id']} already exist, assign another ID",
                                status_code=status.HTTP_409_CONFLICT)
        self.data.append(new_book)
        return new_book



