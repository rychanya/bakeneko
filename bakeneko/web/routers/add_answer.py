from fastapi import APIRouter

from bakeneko.db import session_factory
from bakeneko.db.answer_crud import add_answer
from bakeneko.models.add_answer import AddAnswer, AddAnswerResponse

router = APIRouter(prefix="/add-answer", tags=["add answer"])


@router.post("/", response_model=AddAnswerResponse)
def add_answer_rout(dto: AddAnswer):
    with session_factory() as session:
        response = add_answer(dto=dto, session=session)
    return response
