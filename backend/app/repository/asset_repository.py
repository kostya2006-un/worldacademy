from sqlalchemy import select, delete
from dp import async_session
from schemas import AssetSchema
from models import Assets


class AssetsRepository:
    @classmethod
    async def add_asset(cls, asset_data: AssetSchema) -> str:
        async with async_session() as session:
            asset = Assets(**asset_data.model_dump())
            session.add(asset)
            await session.commit()
            return asset.ticker

    @classmethod
    async def delete_asset(cls, asset_ticker: str) -> bool:
        async with async_session() as session:
            result = await session.execute(
                delete(Assets).where(Assets.ticker == asset_ticker)
            )
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def get_asset(cls, asset_ticker: str):
        async with async_session() as session:
            result = await session.execute(
                select(Assets).where(Assets.ticker == asset_ticker)
            )
            asset_model = result.scalar_one_or_none()
            return (
                AssetSchema.model_validate(asset_model.__dict__)
                if asset_model
                else None
            )

    @classmethod
    async def all_assets(cls) -> list[AssetSchema]:
        async with async_session() as session:
            result = await session.execute(select(Assets))
            return [
                AssetSchema.model_validate(asset.__dict__)
                for asset in result.scalars().all()
            ]
