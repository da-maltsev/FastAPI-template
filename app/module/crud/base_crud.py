from typing import Generic, Optional, Type, TypeVar

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.session = session
        self.model = model

    async def get(self, id: int) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement=statement)
        obj = results.scalar_one_or_none()  # type: ModelType | None

        if obj is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Hasn't been found!",
            )

        return obj

    async def get_all(self) -> list[ModelType]:
        statement = select(self.model)
        results = await self.session.execute(statement=statement)
        to_return = results.scalars().all()  # type: list[ModelType]

        return to_return

    async def create_many(self, data_list: list[CreateSchemaType]) -> bool:
        for data in data_list:
            values = data.dict()

            new_obj = self.model(**values)
            search_for_duplicate = select(self.model).where(
                self.model.title == new_obj.title
            )
            search = await self.session.execute(search_for_duplicate)
            result = search.scalar_one_or_none()  # type: ModelType | None
            if result is None:
                self.session.add(new_obj)
            else:
                upd_obj = await self.get(id=result.id)
                for k, v in values.items():
                    setattr(upd_obj, k, v)
                self.session.add(upd_obj)

        await self.session.commit()

        return True

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in)  # type: ignore
        self.session.add(db_obj)
        await self.session.commit()  # 5
        await self.session.refresh(db_obj)
        return db_obj

    async def patch(self, id: int, data: UpdateSchemaType) -> ModelType:
        upd_obj = await self.get(id=id)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(upd_obj, k, v)

        self.session.add(upd_obj)
        await self.session.commit()
        await self.session.refresh(upd_obj)

        return upd_obj

    async def delete(self, id: int) -> bool:
        statement = delete(self.model).where(self.model.id == id)

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
