from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class Users(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserPublic(SQLModel):
    id: int
    username: str
    email: str


class TodoBase(SQLModel):
    title: str
    description: str


class Todos(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    title: str
    description: str
