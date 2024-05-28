from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import functions

from src.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4())
    username: Mapped[str] = mapped_column(sa.String(length=64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(sa.String(length=64), nullable=False, unique=True)
    _hashed_password: Mapped[str] = mapped_column(sa.String(length=1024), nullable=True)
    _hash_salt: Mapped[str] = mapped_column(sa.String(length=1024), nullable=True)
    is_verified: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    is_logged_in: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=functions.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sa.schema.FetchedValue(for_update=True),
    )

    __mapper_args__ = {"eager_defaults": True}

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def set_hashed_password(self, hashed_password: str) -> None:
        self._hashed_password = hashed_password  # type: ignore

    @property
    def hash_salt(self) -> str:
        return self._hash_salt

    def set_hash_salt(self, hash_salt: str) -> None:
        self._hash_salt = hash_salt  # type: ignore
