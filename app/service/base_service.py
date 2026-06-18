from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class BaseService:
    def __init__(self, model: type[SQLModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def _get(self, uid: str):
        return await self.session.get(self.model, uid)

    async def _add(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _update(self, entity: SQLModel):
        return await self._add(entity=entity)

    async def _delete(self, entity: SQLModel):
        await self.session.delete(entity)
        await self.session.commit()
