from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BookModel(BaseModel):
    bk_id: str
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseSettings):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
