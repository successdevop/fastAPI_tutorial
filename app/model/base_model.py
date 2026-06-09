from sqlmodel import SQLModel, Field


class User(SQLModel):
    user_name: str = Field(nullable=False, unique=True, index=True, min_length=3, max_length=16)
    email: str = Field(nullable=False, index=True, unique=True)
    password_hash: str = Field(nullable=False)