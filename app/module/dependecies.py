from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_async_session
from app.module.crud.user_crud import UserCRUD
from app.module.models.user import User


async def get_users_crud(
    session: AsyncSession = Depends(get_async_session),
) -> UserCRUD:
    return UserCRUD(model=User, session=session)
