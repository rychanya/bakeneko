from fastapi import FastAPI

from bakeneko.store import store
from bakeneko.web.routes import config_routes
from bakeneko.web.static import config_static_files

app = FastAPI(on_startup=(store.setup,))
config_static_files(app)
config_routes(app)
