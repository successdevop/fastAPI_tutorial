from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
import uuid


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
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )

    updated_at: datetime = Field(
        default_factory=lambda : datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )

    def __repr__(self):
        return f"<Book(title:{self.title} | author:{self.author} | id:{self.bk_id})>"

