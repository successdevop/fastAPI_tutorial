from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer, Field


class BaseDeliverySchema(BaseModel):
    del_id: str = Field(description="Delivery partner unique ID")
    user_name: str = Field(description="Delivery partner unique username")
    email: str = Field(description="Delivery partner unique email")
    password_hash: str = Field(description="Delivery partner password", exclude=True)
    created_at: datetime = Field(description="Date time at which Seller account was created")
    updated_at: datetime = Field(description="Date time at which Seller account was updated")

    @field_serializer("created_at", "updated_at")
    def serialize_fields(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    class Config:
        from_attributes = True


class UpdateDeliverySchema(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=16)
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None, min_length=8)


class CreateDeliverySchema(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=8)
