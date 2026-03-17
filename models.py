from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: EmailStr
    password: str


class Users(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    password: str


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class UserPublic(SQLModel):
    id: int
    username: str
    email: EmailStr


class TodoBase(SQLModel):
    title: str
    description: str


class Todos(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    title: str
    description: str


class TodoPublic(SQLModel):
    id: int
    title: str
    description: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
