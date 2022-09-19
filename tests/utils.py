import time
import traceback

from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.core import config
from testcontainers.core.container import DockerContainer
from testcontainers.core.exceptions import TimeoutException
from testcontainers.core.utils import setup_logger
from testcontainers.postgres import PostgresContainer

from bakeneko.store.SQLStore.settings import settings

logger = setup_logger(__name__)
transient_exceptions = (TimeoutError, ConnectionError, DBAPIError)


class AsyncPostgresContainer(PostgresContainer):
    def __init__(self):
        super(PostgresContainer, self).__init__(image="postgres:latest")
        self.POSTGRES_USER = settings.username
        self.POSTGRES_PASSWORD = settings.password
        self.POSTGRES_DB = settings.database
        self.port_to_expose = settings.port
        self.driver = settings.driver

        self.ports[5432] = settings.port

    async def __aenter__(self):
        self._configure()
        DockerContainer.start(self)
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    async def _connect(self):
        engine = create_async_engine(self.get_connection_url())
        exception = None
        logger.info("Waiting to be ready...")
        for attempt_no in range(config.MAX_TRIES):
            try:
                async with engine.begin() as connection:
                    return connection
            except transient_exceptions as e:
                logger.debug(
                    f"Connection attempt '{attempt_no + 1}' of '{config.MAX_TRIES + 1}' "
                    f"failed: {traceback.format_exc()}"
                )
                time.sleep(config.SLEEP_TIME)
                exception = e
        raise TimeoutException(
            f"Wait time ({config.MAX_TRIES * config.SLEEP_TIME}s)"
            f"Exception: {exception}"
        )
