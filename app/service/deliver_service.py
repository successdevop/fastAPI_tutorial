import re
from typing import Tuple, Any

from asyncpg import IntegrityConstraintViolationError
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.redis_conn import add_jti_to_blacklist

from app.auth.auth_utils import generate_passwd_hash, verify_password, generate_token
from app.model.delivery_model import DeliveryPartner
from app.schemas.seller_shema import CreateSellerSchema



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
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain at least one capital letter and one small letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        if not any(c in SPECIAL_CHARS for c in password):
            return False, "Password must contain at least one special character"

        return True, "OK"

    async def _partner_already_exist(self, email: str = None, username: str = None, session: AsyncSession = None) -> Tuple[bool, str, Any]:
        """Check if email or username already exists in database"""

        if session is None:
            raise ValueError("Session cannot be None")

        # Check if email exists
        if email is not None:
            email_statement = select(DeliveryPartner).where(DeliveryPartner.email == email)
            email_result = await session.exec(email_statement)
            email_exists = email_result.first()

            if email_exists:
                return True, f"Seller with email ({email}) already exists", email_exists

        # Check if username exists
        if username is not None:
            username_statement = select(DeliveryPartner).where(DeliveryPartner.user_name == username)
            username_result = await session.exec(username_statement)
            username_exists = username_result.first()

            if username_exists:
                return True, f"Seller with username ({username}) already exists", username_exists

        # Neither exists
        return False, "Not found", None

    async def get_all_delivery_partners(self, session: AsyncSession):
        result = await session.exec(select(DeliveryPartner))
        return result.all()

    async def register_delivery_partner(self, req_body: CreateSellerSchema, session: AsyncSession) -> DeliveryPartner:
        if not self._validate_email(req_body.email):
            raise HTTPException(detail="Invalid email format", status_code=status.HTTP_401_UNAUTHORIZED)

        bool_Val, str_Val = self._validate_password(req_body.password)
        if not bool_Val:
            raise HTTPException(detail=str_Val, status_code=status.HTTP_401_UNAUTHORIZED)

        exist_, exist_val, _ = await self._partner_already_exist(email=req_body.email, username=req_body.username, session=session)
        if exist_:
            raise HTTPException(detail=exist_val, status_code=status.HTTP_409_CONFLICT)

        partner_data = req_body.model_dump()
        new_partner = DeliveryPartner(**partner_data, user_name=partner_data["username"])
        new_partner.password_hash = generate_passwd_hash(partner_data["password"])

        try:
            session.add(new_partner)
            await session.commit()
            await session.refresh(new_partner)
            return new_partner
        except IntegrityConstraintViolationError as error:
            await session.rollback()
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            await session.rollback()
            raise HTTPException(detail=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def login_func(self, email: str, password, session: AsyncSession) -> dict[str, Any]:
        _, _, d_partner = await self._partner_already_exist(email=email, session=session)

        if d_partner is None or not verify_password(password=password, hashed_password=d_partner.password_hash):
            raise HTTPException(detail="Invalid email or password", status_code=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(
            user_data={
                "id":d_partner.dlv_id,
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