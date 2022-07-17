from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from bakeneko.config import settings

engine = create_engine(url=settings.db_url, future=True, echo=True)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)


def wait_until_db_ready():
    is_not_ready = True
    while is_not_ready:
        try:
            with engine.connect():
                is_not_ready = False
        except SQLAlchemyError:
            sleep(0.5)
