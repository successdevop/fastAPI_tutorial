from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, INTEGER, ARRAY
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, Relationship

from app.model.base_model import User
from app.model.shipment_model import ShipmentStatus

if TYPE_CHECKING:
    from app.model.shipment_model import Shipment


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER))
    )

    max_handling_capacity: int = Field(default=5, nullable=False)

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    shipments: list["Shipment"] = Relationship(back_populates="delivery", sa_relationship_kwargs={"lazy":"selectin"})

    @property
    def active_shipments(self) -> list["Shipment"]:
        if not self.shipments:
            return []

        active = []
        for shipment in self.shipments:
            if not shipment.timeline:
                active.append(shipment)
            else:
                last_event = shipment.timeline[-1]
                if last_event.status != ShipmentStatus.DELIVERED or last_event.status != ShipmentStatus.CANCELLED:
                    active.append(shipment)
        return active

    @property
    def current_handling_capacity(self) -> int:
        return self.max_handling_capacity - len(self.active_shipments)