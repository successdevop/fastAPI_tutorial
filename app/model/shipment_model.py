import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Relationship, SQLModel, Field, Column


if TYPE_CHECKING:
    from app.model.seller_model import Seller
    from app.model.delivery_model import DeliveryPartner


def get_current_time() -> datetime:
    return datetime.now(tz=timezone.utc)


class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    OUT_OF_DELIVERY = "out_of_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    ship_id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False
    )

    content: str = Field(nullable=False)
    weight: float = Field(nullable=False)
    destination: int = Field(nullable=False)
    timeline: list["ShipmentEvent"] = Relationship(back_populates="shipment",
                                                   sa_relationship_kwargs={"lazy":"selectin", "cascade": "all, delete-orphan"})

    client_contact_email: str | None = Field(default=None)
    client_contact_phone: int | None = Field(default=None)

    created_at: datetime = Field(
        default_factory=get_current_time,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )

    seller_id: str = Field(foreign_key="seller.id", nullable=False, ondelete="CASCADE")
    seller: "Seller" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"})

    del_partner_id: Optional[str] = Field(default=None, foreign_key="delivery_partner.id")
    delivery: "DeliveryPartner" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy":"selectin"})

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None

    def __repr__(self):
        return f"Shipment<(id:{self.ship_id} | status:{self.destination})>"


class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_event"

    s_evt_id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False
    )

    created_at: datetime = Field(
        default_factory=get_current_time,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )

    status: ShipmentStatus = Field(default=ShipmentStatus.PLACED, nullable=False)
    location: int = Field(default=None)
    description: Optional[str] = Field(default=None)
    shipment_id: str = Field(foreign_key="shipment.ship_id", nullable=False, ondelete="CASCADE")
    shipment: "Shipment" = Relationship(back_populates="timeline", sa_relationship_kwargs={"lazy":"selectin"})
