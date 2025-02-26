from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
