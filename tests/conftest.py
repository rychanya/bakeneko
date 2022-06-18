import pytest
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def engine():
    with PostgresContainer() as postgres:
        yield create_engine(url=postgres.get_connection_url(), echo=True, future=True)
