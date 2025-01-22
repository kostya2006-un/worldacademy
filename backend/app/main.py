from fastapi import FastAPI
from dp import init_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()