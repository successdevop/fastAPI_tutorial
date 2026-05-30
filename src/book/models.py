from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
import uuid


def get_current_datetime()-> datetime:
    return datetime.now(tz=timezone.utc)


class Book(SQLModel, table=True):
    __tablename__ = "books"

    bk_id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False
    )
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    publisher: str = Field(nullable=False)
    published_date: str = Field(nullable=False)
    page_count: int = Field(nullable=False)
    language: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )

    updated_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, onupdate=get_current_datetime)
    )

    def __repr__(self):
        return f"<Book(title:{self.title} | author:{self.author} | id:{self.bk_id})>"

