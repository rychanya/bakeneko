from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_engine(db_url: str):
    return create_engine(url=db_url, echo=True, future=True)
