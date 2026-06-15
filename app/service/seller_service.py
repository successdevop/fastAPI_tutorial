from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.redis_conn import add_jti_to_blacklist

from app.model.seller_model import Seller
from app.schemas.seller_shema import CreateSellerSchema
from app.service.user_service import UserService


class SellerService(UserService):
    def __init__(self, session:AsyncSession):
        super().__init__(model=Seller, session=session)

    async def get_all_sellers(self):
        result = await self.session.exec(select(self.model))
        return result.all()

    async def register_seller(self, req_body: CreateSellerSchema) -> Seller:
        data = req_body.model_dump()
        result = await self._add_user(user_data=data)
        return result


    async def login_func(self, email: str, password) -> dict[str, Any]:
        token = await self._generate_token(email=email, password=password)

        return {
            "message":"Login successful",
            "access_token":token,
            "type":"jwt"
        }

    async def logout(self, token_data: dict):
        await add_jti_to_blacklist(jti=token_data["jti"])
        return {"message":"Successfully logged out"}