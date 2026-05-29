from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid


class Book(SQLModel, table=True):
    bk_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, index=True, default=lambda : str(uuid.uuid4())))
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=lambda : datetime.now(tz=timezone.utc)))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=lambda : datetime.now(tz=timezone.utc)))

    def __repr__(self):
        return f"<Book(title:{self.title} | author:{self.author} | id:{self.bk_id})>"