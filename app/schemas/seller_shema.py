from datetime import datetime

from pydantic import BaseModel, field_serializer, Field


class BaseSellerSchema(BaseModel):
    seller_id: str = Field(description="Seller unique ID")
    user_name: str = Field(description="Seller unique username")
    email: str = Field(description="Seller unique email")
    password_hash: str = Field(description="Seller password", exclude=True)
    created_at: datetime = Field(description="Date time at which Seller account was created")
    updated_at: datetime = Field(description="Date time at which Seller account was updated")

    @field_serializer("created_at", "updated_at")
    def serialize_fields(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    class Config:
        from_attributes = True

class LoginSellerModel(BaseModel):
    email: str | None = Field(default=None)
    password_hash: str = Field(default=None, min_length=8)


class UpdateSellerSchema(BaseModel):
    user_name: str | None = Field(default=None, min_length=3, max_length=16)
    email: str | None = Field(default=None)
    password_hash: str = Field(default=None, min_length=8)


class CreateSellerSchema(BaseModel):
    user_name: str = Field(min_length=3, max_length=16)
    email: str
    password_hash: str = Field(min_length=8)
