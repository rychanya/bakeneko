from sqlalchemy import create_engine


def get_engine(db_url: str, echo: bool = False):
    return create_engine(url=db_url, future=True, echo=echo)
