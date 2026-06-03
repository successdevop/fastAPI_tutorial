from enum import Enum

from pydantic import BaseModel, Field


class ShipmentStatus(Enum):
    PLACED = "places"
    IN_TRANSIT = "in_transit"
    OUT_OF_DELIVERY = "out_of_delivery"
    DELIVERED = "delivered"


class Shipment(BaseModel):
    content: str = Field(
        description="The contents of the shipment",
        max_length=30
    )
    weight: float = Field(
        description="Weight of shipment in kilograms (kgs)",
        le=25,
        ge=1
    )
    status: str | None = Field(
        description="Destination zipcode",
        default=None
    )