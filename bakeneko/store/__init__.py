from bakeneko.settings import StoreType, app_settings
from bakeneko.store.base import BaseStore
from bakeneko.store.SQLStore import SQLStore
from bakeneko.store.SQLStore.settings import settings


def init_store() -> BaseStore:
    match app_settings.store_type:
        case StoreType.SQLStore:
            return SQLStore(db_url=settings.db_url, echo=settings.echo)
        case _:
            raise ValueError


store = init_store()
