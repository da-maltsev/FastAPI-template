from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select

from app.module.crud.base_crud import CRUDBase
from app.module.models.user import User, UserCreate, UserUpdate


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    async def create_many(self, data_list: list[UserCreate]) -> bool:
        for data in data_list:
            values = data.dict()
            new_user = User(**values)
            search_for_duplicate = select(User).where(User.name == new_user.name)
            search = await self.session.execute(search_for_duplicate)
            result = search.scalar_one_or_none()  # type: User | None
            if result is None:
                self.session.add(new_user)
        await self.session.commit()

        return True

    async def get_by_name(self, name: str) -> User:
        statement = select(User).where(User.name == name)
        results = await self.session.execute(statement=statement)
        some_user = results.scalar_one_or_none()  # type: User | None

        if some_user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!",
            )

        return some_user
