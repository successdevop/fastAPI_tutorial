from datetime import datetime

from pydantic import BaseModel, field_serializer, Field
from pydantic.v1 import EmailStr


class BaseSellerSchema(BaseModel):
    seller_id: str = Field(description="Seller unique ID")
    user_name: str = Field(description="Seller unique username")
    email: EmailStr = Field(description="Seller unique email")
    password_hash: str = Field(description="Seller password")
    created_at: datetime = Field(description="Date time at which Seller account was created")
    updated_at: datetime = Field(description="Date time at which Seller account was updated")

    @field_serializer("created_at", "updated_at")
    def serialize_fields(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    class Config:
        from_attributes = True


class UpdateSellerSchema(BaseModel):
    user_name: str | None = Field(default=None, ge=3, le=16)
    email: EmailStr | None = Field(default=None)
    password_hash: str = Field(default=None, ge=8)


class CreateSellerSchema(BaseModel):
    user_name: str = Field(ge=3, le=16)
    email: EmailStr
    password_hash: str = Field(ge=8)
