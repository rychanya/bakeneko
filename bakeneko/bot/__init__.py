import asyncio

from loguru import logger


async def test_as():
    n = 0

    while True:
        try:
            await asyncio.sleep(1)
            n = n + 1
            logger.info(f"{n} task loguru")
        except asyncio.CancelledError:
            break
