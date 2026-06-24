import uuid
from datetime import timedelta, datetime, timezone
from typing import Any, Optional

import jwt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from passlib.context import CryptContext

from app.config import security_settings


_serializer = URLSafeTimedSerializer(security_settings.JWT_SECRET)


def generate_passwd_hash(password: str) -> str:
    pw_ctx = CryptContext(schemes=["bcrypt"])
    return pw_ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    pw_ctx = CryptContext(schemes=["bcrypt"])
    return pw_ctx.verify(password, hashed_password)


def generate_token(user_data: dict, expiry: timedelta | None = None) -> str:
    access_token_expiry: int = 1800

    payload = {
        "user":user_data,
        "exp": datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(seconds=access_token_expiry)),
        "jti": str(uuid.uuid4())
    }

    token = jwt.encode(
        payload=payload,
        key=security_settings.JWT_SECRET,
        algorithm=security_settings.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None


def generate_url_safe_token(data: dict, salt: str | None = None) -> str:
    return _serializer.dumps(data, salt=salt)


def decode_url_safe_token(token: str, salt: str | None = None, expiry: timedelta | None = None) -> dict | None:
    try:
        return _serializer.loads(
            s=token,
            salt=salt,
            max_age=int(expiry.total_seconds()) if expiry else None
        )
    except (BadSignature | SignatureExpired):
        return None
