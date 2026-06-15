from typing import Annotated

from fastapi import Depends

from app.database.session import SessionDep
from app.service.deliver_service import DeliveryService


async def get_delivery_service(session: SessionDep):
    return DeliveryService(session=session)

DeliveryServiceDep = Annotated[DeliveryService, Depends(get_delivery_service)]