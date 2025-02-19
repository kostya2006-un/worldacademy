import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from models import Assets
from dp import async_session
from sqlalchemy import select


async def update_write_price_assets():
    async with async_session() as session:
        async with httpx.AsyncClient() as client:
            res = await session.execute(select(Assets))
            assets = res.scalars().all()
            for asset in assets:
                ticker = f"{asset.ticker}USDT"
                try:
                    response = await client.get(f"https://api.binance.us/api/v3/ticker/price?symbol={ticker}")
                    data = response.json()
                    new_price = round(float(data["price"]), 2)

                    asset.price = new_price
                    session.add(asset)
                except Exception as e:
                    print(f"Ошибка обновления {ticker}: {e}")
            await session.commit()

scheduler = AsyncIOScheduler()


def start_scheduler():
    """Запускаем планировщик для обновления цен активов."""
    scheduler.add_job(update_write_price_assets, "interval", seconds=120)  # Каждые 2 минуты
    scheduler.start()