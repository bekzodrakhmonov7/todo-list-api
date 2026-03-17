from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select

from db import SessionDep, db_engine
from models import UserBase, UserLogin, UserPublic, Users

app = FastAPI()


SQLModel.metadata.create_all(db_engine)


@app.get("/health")
def return_health():
    return {"Success": True}


# TODO
@app.post("/register", response_model=dict[str, bool | UserPublic])
def create_user(user: UserBase, session: SessionDep):
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
    return {"success": True, "details": db_user}


@app.post("/login", response_model=dict[str, bool | UserPublic])
def login(user: UserLogin, session: SessionDep):
    statement = select(Users).where(Users.email == user.email)
    try:
        result = session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username or password incorrect",
            )
        return {"success": True, "details": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred, {e}",
        )
