from pprint import pprint

from telegram import Bot, MenuButtonWebApp, WebAppInfo

from bakeneko.bot.models import Update
from bakeneko.config import settings

bot = Bot(settings.TG_TOKEN)


async def init_bot():
    await bot.set_webhook(settings.web_hook_url)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Меню", web_app=WebAppInfo(url=settings.web_app_menu_url)
        )
    )


async def handle_update(update_row: dict):
    pprint(update_row)
    update = Update.parse_obj(update_row)
    print(update)
