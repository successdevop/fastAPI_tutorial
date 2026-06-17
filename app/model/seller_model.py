from typing import List, TYPE_CHECKING
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Relationship, Field, Column
from app.model.base_model import User

if TYPE_CHECKING:
    from app.model.shipment_model import Shipment


class Seller(User, table=True):
    __tablename__ = "seller"

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    updated_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, onupdate=lambda : datetime.now(tz=timezone.utc))
    )
    shipments: List["Shipment"] = Relationship(back_populates="seller", sa_relationship_kwargs={"lazy":"selectin"})
    