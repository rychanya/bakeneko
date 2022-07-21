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
            title=f"{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            description="1 fjvjindnenvnuenuvnru\n2 dfejn efrefr efdvdever ervvevev ergeg\3 fkgn",
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
