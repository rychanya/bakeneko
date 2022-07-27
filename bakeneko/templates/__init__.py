from urllib.parse import urlparse, urlunparse

from fastapi.templating import Jinja2Templates
from starlette.datastructures import URL

templates = Jinja2Templates(directory="bakeneko/templates")


def https(value: str | URL):
    if isinstance(value, URL):
        value = str(value)
    parts = urlparse(value)
    return urlunparse(["https", *parts[1:]])


templates.env.filters["https"] = https
