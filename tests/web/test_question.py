import pytest
from httpx import AsyncClient

from bakeneko.models.types import TypeEnum


@pytest.mark.anyio
async def test_root2(app_fix):
    url = app_fix.url_path_for("get_or_create_question")
    json_data = {
        "question_type": TypeEnum.ONE,
        "text": "text",
        "all_answers": [],
        "all_extra_answers": [],
    }

    async with AsyncClient(app=app_fix, base_url="http://test") as ac:
        response1 = await ac.post(
            url,
            json=json_data,
        )

    async with AsyncClient(app=app_fix, base_url="http://test") as ac:
        response2 = await ac.post(url, json=json_data)

    assert response1.status_code == 201
    assert response2.status_code == 200
    assert response1.json() == response2.json()
