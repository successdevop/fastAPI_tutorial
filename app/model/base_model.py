import uuid

from sqlmodel import SQLModel, Field


class User(SQLModel):
    id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True,
        nullable=False,
        index=True)

    user_name: str = Field(nullable=False, unique=True, index=True, min_length=3, max_length=16)
    email: str = Field(nullable=False, index=True, unique=True)
    email_verified: bool = Field(default=False)
    password_hash: str = Field(nullable=False)