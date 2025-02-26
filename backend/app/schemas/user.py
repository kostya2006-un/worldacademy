from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class UserUpdate(BaseModel):
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    is_bot: bool = False
    is_active: Optional[bool] = True
    is_premium: Optional[bool] = False
    language_code: Optional[str]
    balance: float | None = None


class UserBase(BaseModel):
    id_user: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    is_bot: bool = False
    is_active: Optional[bool] = True
    is_premium: Optional[bool] = False
    language_code: Optional[str]
    balance: float


class UserResponse(UserBase):
    created_at: datetime
    balance: float

    class Config:
        orm_mode = True


class UserList(BaseModel):
    id_user: int