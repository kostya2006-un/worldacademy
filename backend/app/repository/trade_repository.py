from dp import async_session
from models import Trade
from sqlalchemy.future import select


class TradeRepository:
    @staticmethod
    async def create_trade(user_id: int, ticker: str, trade_type: str, quantity: float, price: float):
        async with async_session() as session:
            trade = Trade(id_user=user_id, ticker=ticker, trade_type=trade_type, quantity=quantity, price=price)
            session.add(trade)
            await session.commit()
            return trade

    @staticmethod
    async def get_trade_history(user_id: int):
        async with async_session() as session:
            result = await session.execute(select(Trade).where(Trade.id_user == user_id))
            return result.scalars().all()
