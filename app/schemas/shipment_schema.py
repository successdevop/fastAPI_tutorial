from datetime import datetime
from random import randint

from pydantic import BaseModel, Field, field_serializer
from app.model.shipment_model import ShipmentStatus


class BaseShipmentModel(BaseModel):
    id: str = Field(
        description="The shipment's unique ID"
    )
    content: str = Field(
        description="The contents of the shipment",
    )
    weight: float = Field(
        description="Weight of shipment in kilograms (kgs)",
        ge=1
    )
    destination: int = Field(
        description="Destination zipcode",
        default_factory=lambda : randint(1111, 2111)
    )
    status: ShipmentStatus = Field(
        description="The shipment delivery status",
        default=ShipmentStatus.PLACED.value
    )
    created_at: datetime = Field(
        description="Shipment creation time"
    )
    updated_at: datetime = Field(
        description="Time at which an existing shipment was updated"
    )

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    class Config:
        from_attributes = True


class ShipmentCreateSchema(BaseModel):
    content: str
    weight: float


class ShipmentUpdateSchema(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None)
    destination: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
