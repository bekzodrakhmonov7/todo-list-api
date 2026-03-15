from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from config import settings

db_url = f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_pass.get_secret_value()}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
print(db_url)
db_engine = create_engine(url=db_url)


def get_session():
    with Session(db_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
