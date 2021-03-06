import pytest
from httpx import AsyncClient

from bakeneko.models.types import TypeEnum
from bakeneko.web import app


@pytest.mark.anyio
@pytest.mark.usefixtures("clear_db")
async def test_root2():
    url = app.url_path_for("get_or_create_question")
    json_data = {
        "question_type": TypeEnum.ONE,
        "text": "text",
        "all_answers": [],
        "all_extra_answers": [],
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response1 = await ac.post(
            url,
            json=json_data,
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response2 = await ac.post(url, json=json_data)

    assert response1.status_code == 201
    assert response2.status_code == 200
    assert response1.json() == response2.json()
