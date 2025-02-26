from sqlalchemy import Boolean, String, BigInteger, DateTime, func, Float, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship

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
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=100000.00, nullable=False)
    portfolios = relationship("Portfolio", back_populates="user")
    trades = relationship("Trade", back_populates="user")


class Assets(Base):
    __tablename__ = "assets"
    ticker: Mapped[str] = mapped_column(String(10), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False)  # stock, crypto, bond
    price: Mapped[float] = mapped_column(Float, nullable=False)

    portfolios = relationship("Portfolio", back_populates="asset")
    trades = relationship("Trade", back_populates="asset")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id_portfolio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(Integer, ForeignKey("users.id_user"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(10), ForeignKey("assets.ticker"), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False, default=0)

    user = relationship("User", back_populates="portfolios")
    asset = relationship("Assets", back_populates="portfolios")


class Trade(Base):
    __tablename__ = "trades"

    id_trade: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(Integer, ForeignKey("users.id_user"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(10), ForeignKey("assets.ticker"), nullable=False)
    trade_type: Mapped[str] = mapped_column(String(10), nullable=False)  # buy / sell
    quantity: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="trades")
    asset = relationship("Assets", back_populates="trades")

