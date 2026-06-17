import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, INTEGER, ARRAY
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, Relationship

from app.model.base_model import User

if TYPE_CHECKING:
    from app.model.shipment_model import Shipment
    from app.model.shipment_model import ShipmentStatus


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER))
    )

    max_handling_capacity: int

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    shipments: list["Shipment"] = Relationship(back_populates="delivery", sa_relationship_kwargs={"lazy":"selectin"})

    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.DELIVERED
        ]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)