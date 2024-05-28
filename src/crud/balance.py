from typing import Sequence
from uuid import UUID

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.redis import async_redis
from src.models.balance import Balance
from src.crud.base import BaseCRUDInterface
from src.models.balance import BalanceTransferHistory
from src.schemas.routes.balance import BalanceUpdateType, BalanceTransferType
from src.utilities.exceptions.database import EntityDoesNotExist


class BalanceCRUDInterface(BaseCRUDInterface):
    async def update_balance(self, balance_update: BalanceUpdateType) -> Balance:
        stmt = sqlalchemy.select(Balance).where(Balance.user_id == balance_update.user_id)
        query = await self.async_session.execute(statement=stmt)
        balance = query.scalar()

        if not balance:
            raise EntityDoesNotExist("Balance for user with id `{id}` does not exist!")

        balance.amount += balance_update.amount

        await self.async_session.commit()
        await self.async_session.refresh(instance=balance)

        await async_redis.set(f"balance:{balance.user_id}", balance.__dict__)

        return balance

    async def transfer_balance(self, balance_transfer: BalanceTransferType) -> BalanceTransferHistory:
        from_stmt = sqlalchemy.select(Balance).where(Balance.user_id == balance_transfer.from_user_id)
        to_stmt = sqlalchemy.select(Balance).where(Balance.user_id == balance_transfer.to_user_id)

        from_query = await self.async_session.execute(statement=from_stmt)
        to_query = await self.async_session.execute(statement=to_stmt)

        from_balance = from_query.scalar()
        to_balance = to_query.scalar()

        if not from_balance or not to_balance:
            raise EntityDoesNotExist("One of the users does not have a balance record!")

        if from_balance.amount < balance_transfer.amount + balance_transfer.fee_amount:
            raise ValueError("Insufficient balance!")

        from_balance.amount -= (balance_transfer.amount + balance_transfer.fee_amount)
        to_balance.amount += balance_transfer.amount

        transfer_history = BalanceTransferHistory(
            balance_id=from_balance.id,
            amount=balance_transfer.amount,
            balance_before=from_balance.amount,
            balance_after=from_balance.amount - balance_transfer.amount,
            operation_type="transfer",
        )

        self.async_session.add(instance=transfer_history)
        await self.async_session.commit()
        await self.async_session.refresh(instance=transfer_history)

        return transfer_history

    async def get_balance_history(self, user_id: UUID) -> Sequence[BalanceTransferHistory]:
        cache_key = f"balance:history:{user_id}"
        cached_history = await async_redis.get(cache_key)
        if cached_history:
            return [BalanceTransferHistory(**record) for record in cached_history]

        balance_stmt = sqlalchemy.select(Balance).where(Balance.user_id == user_id)
        balance_query = await self.async_session.execute(statement=balance_stmt)
        balance = balance_query.scalar()

        if not balance:
            raise EntityDoesNotExist("Balance for user with id `{id}` does not exist!")

        history_stmt = sqlalchemy.select(BalanceTransferHistory).where(BalanceTransferHistory.balance_id == balance.id)
        history_query = await self.async_session.execute(statement=history_stmt)
        history = history_query.scalars().all()

        await async_redis.set(cache_key, [record.__dict__ for record in history])

        return history

