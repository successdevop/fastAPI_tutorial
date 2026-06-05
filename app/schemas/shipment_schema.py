from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from app.model.shipment_model import ShipmentStatus


class BaseShipmentModel(BaseModel):
    ship_id: str = Field(
        description="The shipment's unique ID"
    )
    content: str = Field(
        description="The contents of the shipment",
    )
    weight: float = Field(
        description="Weight of shipment in kilograms (kgs)",
    )
    destination: int = Field(
        description="Destination zipcode",
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
    weight: float = Field(gt=1)


class ShipmentUpdateSchema(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, gt=1)
    destination: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
