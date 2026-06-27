from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_serializer, ConfigDict
from app.model.shipment_model import ShipmentStatus, TagName


class ShipmentEventResponse(BaseModel):
    s_evt_id: str
    created_at: datetime
    status: ShipmentStatus
    location: int
    description: Optional[str] = None
    shipment_id: str

    model_config = ConfigDict(from_attributes=True)


class TagData(BaseModel):
    tag_id: str
    name: TagName
    instruction: str
    model_config = ConfigDict(from_attributes=True)


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
    timeline: List[ShipmentEventResponse] = Field(
        description="A list of shipment events",
        default_factory=list
    )
    tags: List[TagData] = Field(description="A list of shipment tags", default_factory=list)

    created_at: datetime = Field(
        description="Shipment creation time"
    )

    client_contact_email: str | None
    client_contact_phone: str | None

    seller_id: str = Field(
        description="ID of the creator of the shipment"
    )
    del_partner_id: Optional[str] = Field(
        default=None,
        description="ID of the delivery partner of the shipment"
    )

    @field_serializer("created_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

    model_config = ConfigDict(from_attributes=True)


class ShipmentCreateSchema(BaseModel):
    content: str
    weight: float = Field(gt=1)
    destination: int
    client_contact_email: str
    client_contact_phone: str


class ShipmentUpdateSchema(BaseModel):
    status: Optional[ShipmentStatus] = Field(default=None)
    location: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default=None)
    verification_code: str | None = Field(default=None)


class ShipmentReview(BaseModel):
    rating: int | None = Field(ge=1, le=5)
    comment: str | None = Field(default=None)
