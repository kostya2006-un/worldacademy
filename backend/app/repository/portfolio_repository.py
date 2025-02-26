from dp import async_session
from models import Portfolio
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


class PortfolioRepository:
    @staticmethod
    async def get_portfolio(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Portfolio)
                .options(joinedload(Portfolio.asset))
                .where(Portfolio.id_user == user_id)
            )
            portfolios = result.scalars().all()

            return [
                {
                    "ticker": p.ticker,
                    "quantity": float(p.quantity),
                    "total_value": round(float(p.quantity) * float(p.asset.price), 2),
                }
                for p in portfolios
            ]

    @staticmethod
    async def create_update_portfolio(ticker: str, quantity: float, user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Portfolio).where(
                    Portfolio.id_user == user_id, Portfolio.ticker == ticker
                )
            )
            portfolio = result.scalars().first()

            if portfolio:
                portfolio.quantity += quantity
            else:
                session.add(
                    Portfolio(id_user=user_id, ticker=ticker, quantity=quantity)
                )

            await session.commit()
