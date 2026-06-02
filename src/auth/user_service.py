from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from src.auth.user_schemna import UserCreatedModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.user_model import User
from src.utils.utils import UtilsService
from sqlmodel import select


class UserService:
    async def create_user(self, user_data: UserCreatedModel, session: AsyncSession):
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
