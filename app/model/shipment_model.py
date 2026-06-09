import uuid
from datetime import datetime, timezone
from enum import Enum
from random import randint
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Relationship, SQLModel, Field, Column


if TYPE_CHECKING:
    from app.model.seller_model import SellerModel
    from app.model.delivery_model import DeliveryPartner


def get_current_time() -> datetime:
    return datetime.now(tz=timezone.utc)


class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    OUT_OF_DELIVERY = "out_of_delivery"
    DELIVERED = "delivered"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    ship_id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False
    )

    content: str = Field(nullable=False)
    weight: float | int = Field(nullable=False)
    destination: int = Field(default_factory=lambda : randint(2222, 9999), nullable=False)
    status: ShipmentStatus = Field(default=ShipmentStatus.PLACED, nullable=False)

    created_at: datetime = Field(
        default_factory=get_current_time,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )

    updated_at: datetime = Field(
        default_factory=get_current_time,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, onupdate=get_current_time)
    )

    seller_id: str = Field(foreign_key="seller.seller_id")
    seller: "SellerModel" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy":"selectin"})

    del_partner_id: str = Field(foreign_key="delivery_partner.dlv_id")
    delivery: "DeliveryPartner" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"Shipment<(id:{self.ship_id} | status:{self.status})>"