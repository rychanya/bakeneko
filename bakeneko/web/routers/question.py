from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from bakeneko.db.question import get_or_create
from bakeneko.models.question import Question, QuestionInDB
from bakeneko.web.dependencies import engine_depend

router = APIRouter(prefix="/question", tags=["question"])


@router.post(
    "/",
    response_model=QuestionInDB,
    responses={status.HTTP_201_CREATED: {"model": QuestionInDB}},
)
def get_or_create_question(question: Question, engine=Depends(engine_depend)):
    is_new, q = get_or_create(engine, question)
    if is_new:
        status_code = status.HTTP_201_CREATED
    else:
        status_code = status.HTTP_200_OK
    return JSONResponse(status_code=status_code, content=jsonable_encoder(q))
