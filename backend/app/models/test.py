from uuid import uuid4
from sqlmodel import Field, SQLModel
from pydantic import UUID4
from typing import Union


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Union[str, None] = None


class UserBase(SQLModel):
    user_name: str = Field(unique=True)
    email: str
    disabled: Union[bool, None] = None


class User(UserBase, table=True):
    user_id: UUID4 | None = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str

class UserWithPassword(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str
    pass


class UserRead(UserBase):
    pass


class UserUpdate(SQLModel):
    user_name: str | None = None
    email: str | None = None

