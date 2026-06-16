from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer, Field


class BaseDeliverySchema(BaseModel):
    del_id: str = Field(description="Delivery partner unique ID")
    user_name: str = Field(description="Delivery partner unique username")
    email: str = Field(description="Delivery partner unique email")
    password_hash: str = Field(description="Delivery partner password", exclude=True)
    created_at: datetime = Field(description="Date time at which Delivery partner account was created")

    @field_serializer("created_at")
    def serialize_fields(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    class Config:
        from_attributes = True


class UpdateDeliverySchema(BaseModel):
    serviceable_zip_codes: Optional[list[int]] = Field(default=None)
    max_handling_capacity: Optional[int] = Field(default=None)


class CreateDeliverySchema(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=8)
    serviceable_zip_codes: list[int]
    max_handling_capacity: int
