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
            id=str(i),
            title=f"{i} title",
            input_message_content=InputTextMessageContent(message_text=str(i)),
        )
        for i in range(page * 10, (page + 1) * 10)
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
