from redis.asyncio import Redis

from app.config import db_settings


_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=0
)


async def add_jti_to_blacklist(jti: str):
    try:
        await _token_blacklist.set(jti, "blacklist")
    except Exception as e:
        print(f"Redis error | {e}")
        raise


async def is_jti_blacklisted(jti: str) -> bool:
    try:
        return await _token_blacklist.exists(jti) > 0
    except Exception as e:
        print(f"Redis error | {e}")
        return False