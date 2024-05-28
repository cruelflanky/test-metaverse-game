from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, condecimal


class ItemCreateType(BaseModel):
    type_id: UUID
    character_id: UUID | None
    owner_id: UUID | None


class ItemEquipType(BaseModel):
    item_id: UUID
    is_equipped: bool


class ItemType(BaseModel):
    id: UUID
    type_id: UUID
    character_id: UUID | None
    owner_id: UUID | None
    is_equipped: bool


class ItemTransferType(BaseModel):
    item_id: UUID
    from_owner_id: UUID
    to_owner_id: UUID
    fee_amount: condecimal(max_digits=15, decimal_places=2)


class ItemTransferHistoryType(BaseModel):
    id: UUID
    item_id: UUID
    from_owner_id: UUID
    to_owner_id: UUID
    fee_amount: condecimal(max_digits=15, decimal_places=2)
    balance_transfer_history_id: UUID
    created_at: datetime
