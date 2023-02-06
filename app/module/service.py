from fastapi import Depends

from app.module.crud.user_crud import UserCRUD
from app.module.dependecies import get_users_crud
from app.module.models.user import UserOut, UserPage


async def get_user_page(
    users: UserCRUD = Depends(get_users_crud),
) -> UserPage:
    result = await users.get_all()
    return UserPage(count=len(result), users=result)


async def get_user(
    user_id: int,
    users: UserCRUD = Depends(get_users_crud),
) -> UserOut:
    result = await users.get(user_id)
    return result
