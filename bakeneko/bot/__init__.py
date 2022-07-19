from pprint import pprint

from telegram import Bot

from bakeneko.bot.models import Update
from bakeneko.config import settings

bot = Bot(settings.TG_TOKEN)


async def handle_update(update: dict):
    pprint(update)
    print(Update.parse_obj(update))
