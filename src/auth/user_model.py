import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP


def get_current_time():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False
    )

    username: str = Field(nullable=False, index=True, unique=True)
    email: str = Field(nullable=False, index=True, unique=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    is_verified: bool = False

    created_at: datetime = Field(default_factory=get_current_time,
                                 sa_column=Column(TIMESTAMP(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=get_current_time,
                                 sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    def __repr__(self):
        return f"User<(username:{self.username} | email:{self.email} | user_id:{self.user_id})>"