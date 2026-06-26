import re
from datetime import timedelta
from typing import Type, Tuple

from fastapi import HTTPException, status, BackgroundTasks
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import app_settings
from app.notifications.email_service import NotificationService
from app.service.base_service import BaseService
from app.model.base_model import User
from app.auth.auth_utils import verify_password, generate_token, generate_passwd_hash, generate_url_safe_token, \
    decode_url_safe_token


class UserService(BaseService):
    def __init__(self, model: Type[User], session: AsyncSession, task: BackgroundTasks):
        super().__init__(model=model, session=session)
        self._notification = NotificationService(task=task)

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

        if not user.email_verified:
            raise HTTPException(detail="Email not verified", status_code=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(user_data={
            "id": user.id,
            "username": user.user_name
        })

        return token

    async def _add_user(self, user_data: dict, router_prefix: str):
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

        user = await self._add(new_user)

        token = generate_url_safe_token(
            {
                "email": user.email,
                "id": user.id
            }
        )

        self._notification.send_email_message_with_html(
            recipients=[user.email],
            subject_msg="Verify your account with Shipment_App",
            context={
                "username": user.user_name,
                "verification_url": f"http://{app_settings.APP_DOMAIN}/{router_prefix}/verify?token={token}"
            },
            template_name="email_verification_for_registration.html"
        )

        return user

    async def verify_email(self, token: str):
        token_data = decode_url_safe_token(token=token)
        if not token_data:
            raise HTTPException(detail="Invalid token", status_code=status.HTTP_400_BAD_REQUEST)

        u_id = token_data["id"]
        user = await self._get(uid=u_id)
        user.email_verified = True

        await self._update(user)

    async def _delete_user(self, s_id: str):
        user = await self._get(uid=s_id)
        if not user:
            raise HTTPException(detail=f"user with ID ({s_id}) not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        return await self._delete(user)

    async def send_password_reset_link(self, email: str, router_prefix):
        user = await self._get_by_email(email=email)
        if not user:
            raise HTTPException(detail=f"user with email ({email}) not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        token = generate_url_safe_token({"id": user.id}, salt="reset_password")
        self._notification.send_email_message_with_html(
            recipients=[user.email],
            subject_msg="Reset your password",
            context={
                "username": user.user_name,
                "reset_url": f"http://{app_settings.APP_DOMAIN}/{router_prefix}/reset_password?token={token}"
            },
            template_name="reset_password.html"
        )

    async def reset_password(self, token: str, password: str):
        token_data = decode_url_safe_token(
            token=token,
            salt="reset_password",
            expiry=timedelta(days=1)
        )
        if not token_data:
            raise HTTPException(detail="Invalid or expired token", status_code=status.HTTP_400_BAD_REQUEST)

        uid = token_data["id"]
        user = await self._get(uid=uid)
        user.password_hash = generate_passwd_hash(password=password)
        return await self._update(user)


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


