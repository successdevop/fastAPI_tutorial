import re
from typing import Tuple, Any

from asyncpg import IntegrityConstraintViolationError
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.redis_conn import add_jti_to_blacklist

from app.auth.auth_utils import generate_passwd_hash, verify_password, generate_token
from app.model.seller_model import Seller
from app.schemas.seller_shema import CreateSellerSchema



class SellerService:
    async def _already_exist(self,email: str = None, username: str = None,  session: AsyncSession = None) -> Tuple[bool, str, Any]:
        """Check if email or username already exists in database"""

        if session is None:
            raise ValueError("Session cannot be None")

        # Check if email exists
        if email is not None:
            email_statement = select(Seller).where(Seller.email == email)
            email_result = await session.exec(email_statement)
            email_exists = email_result.first()

            if email_exists:
                return True, f"Seller with email ({email}) already exists", email_exists

        # Check if username exists
        if username is not None:
            username_statement = select(Seller).where(Seller.user_name == username)
            username_result = await session.exec(username_statement)
            username_exists = username_result.first()

            if username_exists:
                return True, f"Seller with username ({username}) already exists", username_exists

        # Neither exists
        return False, "Not found", None

    async def get_all_sellers(self, session: AsyncSession):
        result = await session.exec(select(Seller))
        return result.all()

    async def register_seller(self, req_body: CreateSellerSchema, session: AsyncSession) -> Seller:
        if not self._validate_email(req_body.email):
            raise HTTPException(detail="Invalid email format", status_code=status.HTTP_401_UNAUTHORIZED)

        bool_Val, str_Val = self._validate_password(req_body.password)
        if not bool_Val:
            raise HTTPException(detail=str_Val, status_code=status.HTTP_401_UNAUTHORIZED)

        exist_, exist_val, _ = await self._already_exist(email=req_body.email, username=req_body.username, session=session)
        if exist_:
            raise HTTPException(detail=exist_val, status_code=status.HTTP_409_CONFLICT)

        seller_data = req_body.model_dump()
        new_seller = Seller(**seller_data, user_name=seller_data["username"])
        new_seller.password_hash = generate_passwd_hash(seller_data["password"])

        try:
            session.add(new_seller)
            await session.commit()
            await session.refresh(new_seller)
            return new_seller
        except IntegrityConstraintViolationError as error:
            await session.rollback()
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            await session.rollback()
            raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def login_func(self, email: str, password, session: AsyncSession) -> dict[str, Any]:
        _, _, seller = await self._already_exist(email=email, session=session)

        if seller is None or not verify_password(password=password, hashed_password=seller.password_hash):
            raise HTTPException(detail="Invalid email or password", status_code=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(
            user_data={
                "id":seller.seller_id,
                "username":seller.user_name
            }
        )

        return {
            "message":"Login successful",
            "access_token":token,
            "type":"jwt"
        }

    async def logout(self, token_data: dict):
        await add_jti_to_blacklist(jti=token_data["jti"])
        return {"message":"Successfully logged out"}