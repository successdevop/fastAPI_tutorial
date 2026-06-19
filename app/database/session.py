from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import db_settings


engine = create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=True
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db_tables():
    async with engine.begin() as connection:
        from app.model import SQLModel, Seller, Shipment, ShipmentEvent, DeliveryPartner
        await connection.run_sync(SQLModel.metadata.create_all)


# session to interact with the database
async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# session dependency annotation
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
