from pydantic import BaseModel


class PortfolioResponse(BaseModel):
    ticker: str
    quantity: float