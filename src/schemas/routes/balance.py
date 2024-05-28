from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, condecimal


class BalanceUpdateType(BaseModel):
    user_id: UUID
    amount: condecimal(max_digits=15, decimal_places=2)


class BalanceType(BaseModel):
    id: UUID
    user_id: UUID
    amount: condecimal(max_digits=15, decimal_places=2)
    updated_at: datetime


class BalanceTransferType(BaseModel):
    from_user_id: UUID
    to_user_id: UUID
    amount: condecimal(max_digits=15, decimal_places=2)
    fee_amount: condecimal(max_digits=15, decimal_places=2)


class BalanceTransferHistoryType(BaseModel):
    id: UUID
    balance_id: UUID
    amount: condecimal(max_digits=15, decimal_places=2)
    balance_before: condecimal(max_digits=15, decimal_places=2)
    balance_after: condecimal(max_digits=15, decimal_places=2)
    operation_type: str
    created_at: datetime