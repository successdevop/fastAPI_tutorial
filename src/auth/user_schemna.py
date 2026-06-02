from datetime import datetime

from pydantic import BaseModel, field_serializer, Field


class UserModel(BaseModel):
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    is_deleted: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_fields(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    class Config:
        from_attributes = True


class UserCreatedModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=50)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    password_hash: str = Field(min_length=8)


class UserUpdateModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
