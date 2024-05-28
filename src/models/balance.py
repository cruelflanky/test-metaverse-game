from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import functions

from src.models.base import Base


class Balance(Base):
    __tablename__ = "balance"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4())
    user_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("user.id"), nullable=False)
    amount: Mapped[float] = mapped_column(sa.Numeric(15, 2), nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=functions.now(), onupdate=functions.now()
    )


class BalanceTransferHistory(Base):
    __tablename__ = "balance_transfer_history"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4())
    balance_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("balance.id"), nullable=False)
    amount: Mapped[float] = mapped_column(sa.Numeric(15, 2), nullable=False)
    balance_before: Mapped[float] = mapped_column(sa.Numeric(15, 2), nullable=False)
    balance_after: Mapped[float] = mapped_column(sa.Numeric(15, 2), nullable=False)
    operation_type: Mapped[str] = mapped_column(sa.String(length=50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=functions.now()
    )