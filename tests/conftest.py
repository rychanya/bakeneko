import pytest
from testcontainers.postgres import PostgresContainer

from bakeneko.db import get_engine
from bakeneko.db.scheme import Base


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer() as postgres:
        _engine = get_engine(db_url=postgres.get_connection_url(), echo=True)
        Base.metadata.create_all(_engine)
        yield _engine


@pytest.fixture
def clear_db(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
