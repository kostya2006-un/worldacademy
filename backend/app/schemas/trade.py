from datetime import datetime
from pydantic import BaseModel


class TradeRequest(BaseModel):
    user_id: int
    ticker: str
    trade_type: str  # "buy" or "sell"
    quantity: float


class TradeResponse(BaseModel):
    ticker: str
    trade_type: str
    quantity: float
    price: float
    timestamp: datetime