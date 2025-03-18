from fastapi import FastAPI
from backround_tasks import start_scheduler
from dp import init_db
from api import (
    user_router,
    asset_router,
    trade_router,
    lesson_router,
    question_router,
    topic_router,
    answer_router,
    progres_router,
)


app = FastAPI()
app.include_router(user_router)
app.include_router(asset_router)
app.include_router(trade_router)
app.include_router(lesson_router)
app.include_router(topic_router)
app.include_router(question_router)
app.include_router(answer_router)
app.include_router(progres_router)


@app.on_event("startup")
async def startup():
    start_scheduler()
    await init_db()
