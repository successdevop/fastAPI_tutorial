import uuid
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import SQLModel, Field, Column


class SellerModel(SQLModel, table=True):
    __tablename__ = "seller_table"
    seller_id: str = Field(default_factory=lambda : str(uuid.uuid4()), primary_key=True,
                           nullable=False, index=True)
    user_name: str = Field(nullable=False, unique=True, index=True, min_length=3, max_length=16)
    email: str = Field(nullable=False, index=True, unique=True)
    password_hash: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    updated_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, onupdate=lambda : datetime.now(tz=timezone.utc))
    )