from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

from src.auth.user_schemna import UserCreatedModel, LoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.user_model import User
from src.utils.utils import UtilsService
from sqlmodel import select


class UserService:
    REFRESH_TOKEN_EXPIRY = 1

    @staticmethod
    async def create_user(user_data: UserCreatedModel, session: AsyncSession):
        print(user_data, "POINT A")

        user_data_dict = user_data.model_dump()

        sql_statement = select(User).where(User.email == user_data_dict.get("email"))
        email_ = await session.execute(sql_statement)
        exist_ = email_.scalar_one_or_none()
        if exist_:
            raise HTTPException(detail=f"user with email {user_data_dict.get('email')} already exists",
                                status_code=status.HTTP_401_UNAUTHORIZED)

        sql_statement = select(User).where(User.username == user_data_dict.get("username"))
        username_ = await session.execute(sql_statement)
        exist_un = username_.scalar_one_or_none()

        if exist_un:
            raise HTTPException(detail=f"user with username {user_data_dict.get('username')} already exists",
                                status_code=status.HTTP_401_UNAUTHORIZED)

        new_user = User(**user_data_dict)
        print(new_user, "POINT B")

        new_user.password_hash = UtilsService().hash_password_method(user_data_dict.get("password_hash"))
        print(new_user.password_hash, "POINT C")

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(detail=f"Database Integrity error | {e}", status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            await session.rollback()
            raise HTTPException(detail=f"Server Error | {e}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def login_user(login_data: LoginModel, session: AsyncSession):
        email = login_data.email
        password = login_data.password

        sql_statement = select(User).where(User.email == email)
        result = await session.execute(sql_statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)

        if not UtilsService().verify_password_method(password=password, hash_pw=user.password_hash):
            raise HTTPException(detail="Invalid Email or Password", status_code=status.HTTP_401_UNAUTHORIZED)

        access_token = UtilsService.generate_access_token(
            user_data={
                "user_id": user.user_id,
                "email": user.email
            }
        )

        refresh_token = UtilsService.generate_access_token(
            user_data={
                "user_id": user.user_id,
                "email": user.email
            },
            refresh=True,
            expiry=timedelta(days=UserService.REFRESH_TOKEN_EXPIRY)
        )

        return JSONResponse(
            content={
                "message":"Login successful",
                "access_token":access_token,
                "refresh_token":refresh_token,
                "user":{
                    "email": user.email,
                    "user_id": user.user_id
                }
            }
        )
