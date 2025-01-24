from sqlalchemy import Boolean, String, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)
    is_premium: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
