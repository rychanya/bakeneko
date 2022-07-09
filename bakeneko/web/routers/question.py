from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from bakeneko.db import session_factory
from bakeneko.db.question_crud import get_or_create
from bakeneko.models.question import Question, QuestionInDB

router = APIRouter(prefix="/question", tags=["question"])


@router.post(
    "/",
    response_model=QuestionInDB,
    responses={status.HTTP_201_CREATED: {"model": QuestionInDB}},
)
def get_or_create_question(question: Question):
    with session_factory() as session:
        is_new, q = get_or_create(session=session, question=question)
    if is_new:
        status_code = status.HTTP_201_CREATED
    else:
        status_code = status.HTTP_200_OK
    return JSONResponse(status_code=status_code, content=jsonable_encoder(q))
