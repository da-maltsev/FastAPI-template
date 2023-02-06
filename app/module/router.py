from fastapi import APIRouter, Depends

from app.module.models.user import UserOut, UserPage
from app.module.service import get_user, get_user_page

router = APIRouter(prefix="/api/v1")


@router.get("/users", tags=["Users"])
async def list_of_users(
    user_page: UserPage = Depends(get_user_page),
) -> UserPage:
    """
    Выводит список пользователей
    """
    return user_page


@router.get("/users/{user_id}", tags=["Users"])
async def user_info(
    user: UserOut = Depends(get_user),
) -> UserOut:
    """
    Выводит информацию о пользователе:
    id, имя
    """
    return user
