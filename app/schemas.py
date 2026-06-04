from enum import Enum
from random import randint

from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    OUT_OF_DELIVERY = "out_of_delivery"
    DELIVERED = "delivered"


class BaseShipment(BaseModel):
    content: str = Field(
        description="The contents of the shipment",
        max_length=30
    )
    weight: float = Field(
        description="Weight of shipment in kilograms (kgs)",
        le=25,
        ge=0.1
    )
    destination: int = Field(
        description="Destination zipcode",
        default_factory=lambda : randint(1111, 2111)
    )


class ShipmentRead(BaseShipment):
    status: ShipmentStatus


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus
