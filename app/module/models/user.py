from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str = Field(unique=True, max_length=50)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class UserOut(SQLModel):
    id: int
    name: str


class UserPage(SQLModel):
    count: int
    users: list[UserOut]
