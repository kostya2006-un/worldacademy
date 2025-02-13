from fastapi import FastAPI
from dp import init_db
from api import user_router, asset_router


app = FastAPI()
app.include_router(user_router)
app.include_router(asset_router)


@app.on_event("startup")
async def startup():
    await init_db()