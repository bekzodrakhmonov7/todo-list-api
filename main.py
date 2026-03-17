from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select

from db import SessionDep, db_engine
from models import TodoBase, TodoPublic, Todos, UserBase, UserLogin, UserPublic, Users
from security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password_hash,
)

app = FastAPI()


SQLModel.metadata.create_all(db_engine)
bearer = HTTPBearer()


@app.get("/health")
def return_health():
    return {"Success": True}


@app.post("/auth/register", tags=["auth"])
def create_user(user: UserBase, session: SessionDep):
    user.password = hash_password(user.password)
    db_user = Users.model_validate(user)
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email is already taken.",
        )
    access_token = create_access_token(db_user.username)

    return access_token


@app.post("/auth/login", tags=["auth"])
def login(user: UserLogin, session: SessionDep):
    statement = select(Users).where(Users.email == user.email)
    try:
        result = session.exec(statement)
        db_user = result.first()
        if not db_user or not verify_password_hash(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"User with email {user.email} does not exist",
            )

        access_token = create_access_token(db_user.username)
        return access_token

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred, {e}",
        )


@app.get("/auth/me", tags=["auth"], response_model=UserPublic)
def get_current_user(
    session: SessionDep,
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    token = credentials.credentials

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload is invalid"
        )
    statement = select(Users).where(Users.username == username)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists"
        )

    return db_user


@app.post("/todos", response_model=TodoPublic)
def create_todo(
    session: SessionDep,
    todo: TodoBase,
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    token = credentials.credentials

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_username = payload.get("username")
    if not token_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload is invalid"
        )
    statement = select(Users.id).where(Users.username == token_username)
    db_user_id = session.exec(statement).first()
    db_todo = Todos.model_validate(todo)
    db_todo.user_id = db_user_id
    try:
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while creating todo",
        )
    return db_todo
