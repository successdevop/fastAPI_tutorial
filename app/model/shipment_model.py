import uuid
from enum import Enum

from sqlmodel import SQLModel, Field

class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    OUT_OF_DELIVERY = "out_of_delivery"
    DELIVERED = "delivered"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment_table"
    ship_id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False
    )
    content: str = Field(nullable=False)
    weight: float = Field(nullable=False)
    Destination: int = Field(nullable=False)
    status: ShipmentStatus = Field(default=ShipmentStatus.PLACED.value)

    def __repr__(self):
        return f"Shipment<(id:{self.ship_id} | status:{self.status})>"