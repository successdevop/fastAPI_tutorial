import re
from typing import Type, Tuple

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.service.base_service import BaseService
from app.model.base_model import User
from app.auth.auth_utils import verify_password, generate_token, generate_passwd_hash


class UserService(BaseService):
    def __init__(self, model: Type[User], session: AsyncSession):
        super().__init__(model=model, session=session)

    async def _get_by_email(self, email: str) -> User | None:
        return (await self.session.exec(
            select(self.model).where(self.model.email == email)
        )).first()

    async def _get_by_username(self, username) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.user_name == username)
        )

    async def _generate_token(self, email: str, password: str) -> str:
        user = await self._get_by_email(email=email)
        if user is None or not verify_password(password=password, hashed_password=user.password_hash):
            raise HTTPException(detail="Invalid email or password", status_code=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(user_data={
            "id": user.id,
            "username": user.user_name
        })

        return token

    async def _add_user(self, user_data: dict):
        if not self._validate_email(user_data["email"]):
            raise HTTPException(detail="Invalid email format", status_code=status.HTTP_401_UNAUTHORIZED)

        b_val, s_val = self._validate_password(user_data["password"])
        if not b_val:
            raise HTTPException(detail=s_val, status_code=status.HTTP_401_UNAUTHORIZED)

        if await self._get_by_email(user_data["email"]):
            raise HTTPException(detail=f"user with email ({user_data['email']}) already exists",
                                status_code=status.HTTP_401_UNAUTHORIZED)

        if await self._get_by_username(user_data["username"]):
            raise HTTPException(detail=f"user with username ({user_data['username']}) already exists",
                                status_code=status.HTTP_401_UNAUTHORIZED)

        new_user = self.model(
            **user_data,
            user_name=user_data["username"],
            password_hash=generate_passwd_hash(user_data["password"])
        )

        return await self._add(new_user)

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Simple email validation"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def _validate_password(password: str) -> Tuple[bool, str]:
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


