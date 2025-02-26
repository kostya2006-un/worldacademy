from pydantic import BaseModel
from typing import Optional


class AssetSchema(BaseModel):
    ticker: str
    name: str
    asset_type: str
    price: float
