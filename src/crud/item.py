from uuid import UUID

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import BaseCRUDInterface
from src.models.item import Item
from src.schemas.routes.item import ItemCreateType, ItemEquipType, ItemTransferType
from src.models.item import ItemTransferHistory
from src.models.balance import Balance, BalanceTransferHistory
from src.utilities.exceptions.database import EntityDoesNotExist


class ItemCRUDInterface(BaseCRUDInterface):
    async def create_item(self, item_create: ItemCreateType) -> Item:
        new_item = Item(
            type_id=item_create.type_id,
            character_id=item_create.character_id,
            owner_id=item_create.owner_id
        )

        self.async_session.add(instance=new_item)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_item)

        return new_item

    async def equip_item(self, item_equip: ItemEquipType) -> Item:
        stmt = sqlalchemy.select(Item).where(Item.id == item_equip.item_id)
        query = await self.async_session.execute(statement=stmt)
        item = query.scalar()

        if not item:
            raise EntityDoesNotExist("Item with id `{id}` does not exist!")

        item.is_equipped = item_equip.is_equipped

        await self.async_session.commit()
        await self.async_session.refresh(instance=item)

        return item


class ItemTransferHistoryCRUDInterface(BaseCRUDInterface):
    async def transfer_item(self, item_transfer: ItemTransferType) -> ItemTransferHistory:
        from_stmt = sqlalchemy.select(Item).where(Item.id == item_transfer.item_id).where(Item.owner_id == item_transfer.from_owner_id)
        from_query = await self.async_session.execute(statement=from_stmt)
        item = from_query.scalar()

        if not item:
            raise EntityDoesNotExist("Item with id `{id}` does not exist or does not belong to the user!")

        item.owner_id = item_transfer.to_owner_id

        balance_transfer_history_id = await self.transfer_balance(
            from_user_id=item_transfer.from_owner_id,
            to_user_id=item_transfer.to_owner_id,
            amount=item_transfer.amount,
            fee_amount=item_transfer.fee_amount,
        )

        transfer_history = ItemTransferHistory(
            item_id=item.id,
            from_owner_id=item_transfer.from_owner_id,
            to_owner_id=item_transfer.to_owner_id,
            fee_amount=item_transfer.fee_amount,
            balance_transfer_history_id=balance_transfer_history_id,
        )

        self.async_session.add(instance=transfer_history)
        await self.async_session.commit()
        await self.async_session.refresh(instance=transfer_history)

        return transfer_history

    async def transfer_balance(self, from_user_id: UUID, to_user_id: UUID, amount: float, fee_amount: float) -> UUID:
        from_stmt = sqlalchemy.select(Balance).where(Balance.user_id == from_user_id)
        to_stmt = sqlalchemy.select(Balance).where(Balance.user_id == to_user_id)

        from_query = await self.async_session.execute(statement=from_stmt)
        to_query = await self.async_session.execute(statement=to_stmt)

        from_balance = from_query.scalar()
        to_balance = to_query.scalar()

        if not from_balance or not to_balance:
            raise EntityDoesNotExist("One of the users does not have a balance record!")

        if from_balance.amount < amount + fee_amount:
            raise ValueError("Insufficient balance!")

        from_balance.amount -= (amount + fee_amount)
        to_balance.amount += amount

        transfer_history = BalanceTransferHistory(
            balance_id=from_balance.id,
            amount=amount,
            balance_before=from_balance.amount,
            balance_after=from_balance.amount - amount,
            operation_type="transfer",
        )

        self.async_session.add(instance=transfer_history)
        await self.async_session.commit()
        await self.async_session.refresh(instance=transfer_history)

        return transfer_history.id
