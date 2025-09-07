from uuid import uuid4
from sqlmodel import Field, SQLModel
from pydantic import UUID4


class UserBase(SQLModel):
    user_name: str = Field(unique=True)
    email: str


class User(UserBase, table=True):
    user_id: UUID4 | None = Field(default_factory=uuid4, primary_key=True)
    password_hash: str

class UserCreate(UserBase):
    password: str
    pass


class UserRead(UserBase):
    pass


class UserUpdate(SQLModel):
    user_name: str | None = None
    email: str | None = None

