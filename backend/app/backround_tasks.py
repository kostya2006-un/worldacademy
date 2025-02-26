import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from models import Assets
from dp import async_session

# Список активов, которые должны быть в базе
CRYPTO_ASSETS = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "BNB": "Binance Coin",
    "SOL": "Solana",
    "XRP": "XRP",
}


async def update_write_price_assets():
    async with async_session() as session:
        async with httpx.AsyncClient() as client:
            # Получаем все активы из базы
            res = await session.execute(select(Assets))
            assets = {asset.ticker: asset for asset in res.scalars().all()}

            for ticker, name in CRYPTO_ASSETS.items():
                symbol = f"{ticker}USDT"
                try:
                    # Получаем цену с Binance
                    response = await client.get(
                        f"https://api.binance.us/api/v3/ticker/price?symbol={symbol}"
                    )
                    data = response.json()
                    new_price = round(float(data["price"]), 2)

                    if ticker in assets:
                        asset = assets[ticker]
                        asset.price = new_price
                    else:
                        asset = Assets(
                            ticker=ticker,
                            name=name,
                            asset_type="crypto",
                            price=new_price,
                        )
                        session.add(asset)

                except Exception as e:
                    print(f"Ошибка обновления {ticker}: {e}")

            await session.commit()


scheduler = AsyncIOScheduler()


def start_scheduler():
    """Запускаем планировщик для обновления цен активов и создания отсутствующих."""
    scheduler.add_job(
        update_write_price_assets, "interval", seconds=120
    )  # Обновляем каждые 2 минуты
    scheduler.start()
