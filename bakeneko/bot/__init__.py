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
from bakeneko.web.dependencies import CheckInitData

bot = Bot(settings.TG_TOKEN)


async def init_bot(web_hook_url: str, web_app_menu_url: str):
    is_web_hook_set = await bot.set_webhook(web_hook_url)
    print(f"web hook set: {is_web_hook_set}")
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Меню", web_app=WebAppInfo(url=web_app_menu_url)
        )
    )


async def handle_update(update_row: dict):
    update = Update.parse_obj(update_row)
    if update.inline_query:
        if update.inline_query.query:
            await bot.answer_inline_query(
                inline_query_id=update.inline_query.id,
                results=[
                    InlineQueryResultArticle(
                        id=update.inline_query.query,
                        title="Paste",
                        input_message_content=InputTextMessageContent(
                            message_text=update.inline_query.query,
                            parse_mode=None,
                            disable_web_page_preview=False,
                        ),
                    )
                ],
            )


async def select_answer_in_webapp(
    init_data: CheckInitData, answer_id: str, answer_url: str
):
    await bot.answer_web_app_query(
        web_app_query_id=init_data.query_id,
        result=InlineQueryResultArticle(
            id=answer_id,
            title="title",
            input_message_content=InputTextMessageContent(
                message_text=answer_url,
                parse_mode=None,
                disable_web_page_preview=False,
            ),
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text="Share", switch_inline_query=answer_url)
            ),
        ),
    )
