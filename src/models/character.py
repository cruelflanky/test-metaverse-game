from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import functions

from src.models.base import Base


class Character(Base):
    __tablename__ = "character"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4())
    user_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(sa.String(length=50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=functions.now()
    )
