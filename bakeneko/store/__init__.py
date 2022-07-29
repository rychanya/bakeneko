emoji_dict = {True: "🟢", False: "🔴", None: "⚪"}


async def search(q: str):
    return [
        {
            "id": "1",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
        {
            "id": "2",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
        {
            "id": "3",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
        {
            "id": "4",
            "title": "title",
            "type": "type",
            "answers": ["1", "2", "3"],
        },
    ]


async def get_answer_by_id(answer_id):
    return {
        "id": answer_id,
        "title": "title",
        "type": "type",
        "answers": ["1", "2", "3"],
    }
