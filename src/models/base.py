import sqlalchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __table_args__ = {"extend_existing": True}

    metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()
