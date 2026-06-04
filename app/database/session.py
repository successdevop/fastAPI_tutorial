from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings


engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True
)


async def create_db_tables():
    async with engine.begin() as connection:
