from dp import async_session
from models import Portfolio
from sqlalchemy.future import select


class PortfolioRepository:
    @staticmethod
    async def get_portfolio(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Portfolio).where(Portfolio.id_user == user_id)
            )
            return result.scalars().all()

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
