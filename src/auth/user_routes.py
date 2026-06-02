from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.user_schemna import UserModel, UserCreatedModel
from src.auth.user_service import UserService
from src.db.main import get_db_session

user_router = APIRouter()
user_service = UserService()

@user_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreatedModel, session: AsyncSession = Depends(get_db_session)):
    return await user_service.create_user(user_data=user_data, session=session)
