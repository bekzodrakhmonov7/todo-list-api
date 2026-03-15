from fastapi import FastAPI
from sqlmodel import select

from db import SessionDep
from models import UserBase, UserLogin, Users

app = FastAPI()


@app.get("/health")
def return_health():
    return {"Success": True}


@app.post("/register", response_model=Users)
def create_user(user: UserBase, session: SessionDep) -> Users:
    db_user = Users.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# TODO
@app.post("/login", response_model=Users)
def login(user: UserLogin, session: SessionDep):
    statement = select(Users).where(Users.email == user.email)
    result = session.exec(statement)
    return result
