from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dp import get_session
from repository import (
    PortfolioRepository,
    TradeRepository,
    UserRepository,
    AssetsRepository,
)
from schemas import TradeRequest, PortfolioResponse, TradeResponse
from decimal import Decimal
from models import User

from models import Portfolio

router = APIRouter(prefix="/finance", tags=["finance"])


@router.post("/execute")
async def execute_trade(
    trade_data: TradeRequest, session: AsyncSession = Depends(get_session)
):
    user = await session.get(User, trade_data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    asset = await AssetsRepository.get_asset(trade_data.ticker)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    quantity = Decimal(str(trade_data.quantity))
    total_cost = quantity * Decimal(str(asset.price))
    user.balance = Decimal(str(user.balance))

    if trade_data.trade_type == "buy":
        if user.balance < total_cost:
            raise HTTPException(status_code=400, detail="Not enough balance")

        user.balance -= total_cost
        await PortfolioRepository.create_update_portfolio(
            trade_data.ticker, quantity, trade_data.user_id
        )

    elif trade_data.trade_type == "sell":

        # Получаем объект Portfolio напрямую из базы

        result = await session.execute(
            select(Portfolio)
            .where(Portfolio.id_user == trade_data.user_id)
            .where(Portfolio.ticker == trade_data.ticker)
        )

        portfolio_asset = result.scalar_one_or_none()

        # Проверяем наличие и количество

        if not portfolio_asset or portfolio_asset.quantity < quantity:

            raise HTTPException(status_code=400, detail="Not enough assets to sell")

        # Обновляем количество и баланс

        portfolio_asset.quantity -= quantity

        user.balance += total_cost

        # Удаляем запись, если количество стало 0

        if portfolio_asset.quantity == 0:

            await session.delete(portfolio_asset)

            session.add(user)  # Обновляем только пользователя

        else:

            session.add_all([portfolio_asset, user])

    await session.commit()

    trade = await TradeRepository.create_trade(
        trade_data.user_id,
        trade_data.ticker,
        trade_data.trade_type,
        quantity,
        asset.price,
    )

    return {"status": "success", "new_balance": float(user.balance)}


@router.get("/portfolio/{user_id}", response_model=list[PortfolioResponse])
async def get_portfolio(user_id: int):
    portfolio = await PortfolioRepository.get_portfolio(user_id)
    return portfolio


@router.get("/history/{user_id}", response_model=list[TradeResponse])
async def get_trade_history(user_id: int):
    trades = await TradeRepository.get_trade_history(user_id)
    return trades


@router.get("/portfolio_value/{user_id}")
async def get_portfolio_value(user_id: int):
    portfolio = await PortfolioRepository.get_portfolio(user_id)
    total_value = round(sum(asset["total_value"] for asset in portfolio), 2)

    return {"user_id": user_id, "total_portfolio_value": total_value}
