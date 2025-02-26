from fastapi import FastAPI
from backround_tasks import start_scheduler
from dp import init_db
from api import user_router, asset_router, trade_router


app = FastAPI()
app.include_router(user_router)
app.include_router(asset_router)
app.include_router(trade_router)


@app.on_event("startup")
async def startup():
    start_scheduler()
    await init_db()