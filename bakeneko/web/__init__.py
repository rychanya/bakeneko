from fastapi import FastAPI

from bakeneko.web.routers import question

app = FastAPI()
app.include_router(question.router)


@app.get("/")
async def root():
    return {"res": "ok"}
