from typing import List, TYPE_CHECKING
import uuid
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Relationship, Field, Column
from app.model.base_model import User

if TYPE_CHECKING:
    from app.model.shipment_model import Shipment


class SellerModel(User, table=True):
    __tablename__ = "seller"
    seller_id: str = Field(default_factory=lambda : str(uuid.uuid4()), primary_key=True,
                           nullable=False, index=True)

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    updated_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, onupdate=lambda : datetime.now(tz=timezone.utc))
    )
    shipments: List["Shipment"] = Relationship(back_populates="seller", sa_relationship_kwargs={"lazy":"selectin"})
    