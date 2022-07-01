from bakeneko.db import get_engine
from bakeneko.web.config import settings


def engine_depend():
    return get_engine(settings.db_url)
