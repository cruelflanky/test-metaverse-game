from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import functions

from src.models.base import Base


class ItemType(Base):
    __tablename__ = "item_type"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4())
    name: Mapped[str] = mapped_column(sa.String(length=50), nullable=False)
    type: Mapped[str] = mapped_column(sa.String(length=50), nullable=False)
    rarity: Mapped[str] = mapped_column(sa.String(length=50), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text)


class Item(Base):
    __tablename__ = "item"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4())
    type_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("item_type.id"), nullable=False)
    character_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("character.id"), nullable=True)
    owner_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("user.id"), nullable=True)
    is_equipped: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)


class ItemTransferHistory(Base):
    __tablename__ = "item_transfer_history"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4())
    item_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("item.id"), nullable=False)
    from_owner_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("user.id"), nullable=False)
    to_owner_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("user.id"), nullable=False)
    fee_amount: Mapped[float] = mapped_column(sa.Numeric(15, 2), nullable=False)
    balance_transfer_history_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("balance_transfer_history.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=functions.now()
    )
