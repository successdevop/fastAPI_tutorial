import re
from typing import Tuple

from asyncpg import IntegrityConstraintViolationError
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.seller_model import SellerModel
from app.schemas.BaseSellerModel import CreateSellerSchema


class SellerService:
    def _validate_email(self, email: str) -> bool:
        """Simple email validation"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def _validate_password(self, password: str) -> Tuple[bool, str]:
        """Simple password validation (at least 8 chars, 1 number, 1 capital letter, 1 small letter, 1 special char)"""
        MIN_LEN = 8
        MAX_LEN = 128

        # Special characters allowed
        SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if len(password) < MIN_LEN or len(password) > MAX_LEN:
            return False, f"Password must be at least {MIN_LEN} characters long and not exceed {MAX_LEN} characters"
        if not any(c.isupper() for c in password) or not any(c.lower() for c in password):
            return False, "Password must contain at least one capital letter and one small letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        if not any(c in SPECIAL_CHARS for c in password):
            return False, "Password must contain at least one special character"

        return True, "OK"

    async def _already_exist(self, email: str, username: str, session: AsyncSession):
        sql_statement = select(SellerModel).where(SellerModel.email == email)
        result = await session.exec(sql_statement)
        user = result.one_or_none()

        if user:
            return False, f"Seller with email ({email}) already exists"

        if user.user_name == username:
            return False, f"Seller with user_name ({username}) already exists"

        return True, "OK"

    async def create_seller_account(self, req_body: CreateSellerSchema, session: AsyncSession):
        seller_data = req_body.model_dump()
        if not self._validate_email(req_body.email):
            raise HTTPException(detail="Invalid email format", status_code=status.HTTP_401_UNAUTHORIZED)

        bool_Val, str_Val = self._validate_password(req_body.password_hash)
        if not bool_Val:
            raise HTTPException(detail=str_Val, status_code=status.HTTP_401_UNAUTHORIZED)

        exist_, exist_val = await self._already_exist(email=req_body.email, username=req_body.user_name, session=session)
        if exist_:
            raise HTTPException(detail=exist_val, status_code=status.HTTP_409_CONFLICT)

        new_seller = SellerModel(**seller_data)

        try:
            session.add(new_seller)
            await session.commit()
            await session.refresh(new_seller)
        except IntegrityConstraintViolationError as error:
            await session.rollback()
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            await session.rollback()
            raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
