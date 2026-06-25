from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer, Field


class BaseSellerSchema(BaseModel):
    id: str = Field(description="Seller unique ID")
    user_name: str = Field(description="Seller unique username")
    email: str = Field(description="Seller unique email")
    email_verified: bool | None
    password_hash: str = Field(description="Seller password", exclude=True)
    address: str = Field(description="seller's address")
    zip_code: int = Field(description="seller's zip code")
    created_at: datetime = Field(description="Date time at which Seller account was created")
    updated_at: datetime = Field(description="Date time at which Seller account was updated")

    @field_serializer("created_at", "updated_at")
    def serialize_fields(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    class Config:
        from_attributes = True


class UpdateSellerSchema(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=16)
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None, min_length=8)


class CreateSellerSchema(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=8)
    address: str
    zip_code: int
