from pprint import pprint

from telegram import Bot, InlineQueryResultArticle, InputTextMessageContent

from bakeneko.bot.models import Update
from bakeneko.config import settings

bot = Bot(settings.TG_TOKEN)


def fake(page: int):
    if page > 10:
        return
    return [
        InlineQueryResultArticle(
            id=f"{page}_title",
            title=f"{page} title",
            description="",
            input_message_content=InputTextMessageContent(message_text=str(page)),
        ),
        InlineQueryResultArticle(
            id=f"{page}_one",
            title=" ",
            description=f"{page} one",
            input_message_content=InputTextMessageContent(message_text=str(page)),
        ),
        InlineQueryResultArticle(
            id=f"{page}_two",
            title=" ",
            description=f"{page} two",
            input_message_content=InputTextMessageContent(message_text=str(page)),
        ),
        InlineQueryResultArticle(
            id=f"{page}_3",
            title=" ",
            description=f"{page} 3",
            input_message_content=InputTextMessageContent(message_text=str(page)),
        ),
    ]


async def handle_update(update_row: dict):
    pprint(update_row)
    update = Update.parse_obj(update_row)
    if update.inline_query:
        await bot.answer_inline_query(
            inline_query_id=update.inline_query.id,
            results=fake,
            current_offset=update.inline_query.offset,
        )
