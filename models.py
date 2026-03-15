from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class Users(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class TodoBase(SQLModel):
    title: str
    description: str


class Todos(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    title: str
    description: str
