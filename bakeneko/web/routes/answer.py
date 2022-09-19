from fastapi import APIRouter, Depends

from bakeneko.models.store_dto import SearchParams
from bakeneko.web.dependencies.context import AppContext

ROUTER_PREFIX = "/answers"

router = APIRouter(prefix=ROUTER_PREFIX)


@router.post("/")
async def search(q: str, context: AppContext = Depends()):
    data = await context.store.search(SearchParams(q=q))
    return [{"text": answer.text, "id": str(answer.id_)} for answer in data]
