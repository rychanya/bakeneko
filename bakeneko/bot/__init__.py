from pprint import pprint

from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    MenuButtonWebApp,
    WebAppInfo,
)

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
    if update.inline_query:
        if update.inline_query.query:
            await bot.answer_inline_query(
                inline_query_id=update.inline_query.id,
                results=[
                    InlineQueryResultArticle(
                        id=update.inline_query.query,
                        title="Paste",
                        input_message_content=InputTextMessageContent(
                            message_text="mt",
                            parse_mode=None,
                            disable_web_page_preview=False,
                        ),
                        reply_markup=InlineKeyboardMarkup.from_button(
                            InlineKeyboardButton(
                                text="Share", switch_inline_query=update.inline_query.query
                            )
                        ),
                    )
                ],
            )
