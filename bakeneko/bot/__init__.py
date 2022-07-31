from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    MenuButtonWebApp,
    WebAppInfo,
)

from bakeneko.bot.models import (
    CallBackAction,
    CallBackData,
    CallbackQuery,
    InlineQuery,
    Update,
)
from bakeneko.config import settings
from bakeneko.web.dependencies import CheckInitData

bot = Bot(settings.TG_TOKEN)


async def init_bot(web_hook_url: str, web_app_menu_url: str):
    await bot.initialize()
    await bot.set_webhook(web_hook_url)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Меню", web_app=WebAppInfo(url=web_app_menu_url)
        )
    )


async def handle_update_inline_query(inline_query: InlineQuery):
    if inline_query.query:
        await bot.answer_inline_query(
            inline_query_id=inline_query.id,
            results=[
                InlineQueryResultArticle(
                    id=inline_query.query,
                    title="Paste",
                    thumb_url=settings.get_abs_url("/static/wizard.jpg"),
                    input_message_content=InputTextMessageContent(
                        message_text=inline_query.query,
                        parse_mode=None,
                        disable_web_page_preview=False,
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(text="Open bot", url=bot.link)],
                            [
                                InlineKeyboardButton(
                                    text="Up",
                                    callback_data=CallBackData(
                                        action=CallBackAction.VOTE_UP, data="id"
                                    ).json(),
                                ),
                                InlineKeyboardButton(
                                    text="Down",
                                    callback_data=CallBackData(
                                        action=CallBackAction.VOTE_DOWN, data="id"
                                    ).json(),
                                ),
                            ],
                        ]
                    ),
                )
            ],
        )


async def handle_update_callback_query(callback_query: CallbackQuery):
    if callback_query.data:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id, text="ok", show_alert=True
        )


async def handle_update(update_row: dict):
    update = Update.parse_obj(update_row)
    if update.inline_query:
        await handle_update_inline_query(update.inline_query)
    if update.callback_query:
        await handle_update_callback_query(update.callback_query)


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
