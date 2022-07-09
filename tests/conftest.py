import pytest

from bakeneko.db import engine, wait_until_db_ready
from bakeneko.db.scheme import Base


@pytest.fixture(scope="session", autouse=True)
def wait_for_db():
    wait_until_db_ready()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def clear_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
