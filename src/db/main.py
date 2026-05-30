from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.config import Config


engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    future=True
)


async def init_db():
    async with engine.begin() as conn:
        from src.book.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db_session() -> AsyncSession:
    async_session_maker = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session