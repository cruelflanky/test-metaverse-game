from uuid import UUID

import fastapi

from src.crud.balance import BalanceCRUDInterface
from src.crud.base import get_interface
from src.schemas.routes.balance import BalanceUpdateType, BalanceType, BalanceTransferType, BalanceTransferHistoryType

router = fastapi.APIRouter(prefix="/balances", tags=["balances"])


@router.patch(
    path="/update",
    name="balances:update-balance",
    response_model=BalanceType,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_balance(
    balance_update: BalanceUpdateType,
    balance_interface: BalanceCRUDInterface = fastapi.Depends(get_interface(interface_type=BalanceCRUDInterface)),
) -> BalanceType:
    updated_balance = await balance_interface.update_balance(balance_update=balance_update)
    return BalanceType(
        id=updated_balance.id,
        user_id=updated_balance.user_id,
        amount=updated_balance.amount,
        updated_at=updated_balance.updated_at,
    )


@router.post(
    path="/transfer",
    name="balances:transfer-balance",
    response_model=BalanceTransferHistoryType,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def transfer_balance(
    balance_transfer: BalanceTransferType,
    balance_interface: BalanceCRUDInterface = fastapi.Depends(get_interface(interface_type=BalanceCRUDInterface)),
) -> BalanceTransferHistoryType:
    transfer_history = await balance_interface.transfer_balance(balance_transfer=balance_transfer)
    return BalanceTransferHistoryType(
        id=transfer_history.id,
        balance_id=transfer_history.balance_id,
        amount=transfer_history.amount,
        balance_before=transfer_history.balance_before,
        balance_after=transfer_history.balance_after,
        operation_type=transfer_history.operation_type,
        created_at=transfer_history.created_at,
    )


@router.get(
    path="/history/{user_id}",
    name="balances:get-balance-history",
    response_model=list[BalanceTransferHistoryType],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_balance_history(
    user_id: UUID,
    balance_interface: BalanceCRUDInterface = fastapi.Depends(get_interface(interface_type=BalanceCRUDInterface)),
) -> list[BalanceTransferHistoryType]:
    history = await balance_interface.get_balance_history(user_id=user_id)
    return [
        BalanceTransferHistoryType(
            id=record.id,
            balance_id=record.balance_id,
            amount=record.amount,
            balance_before=record.balance_before,
            balance_after=record.balance_after,
            operation_type=record.operation_type,
            created_at=record.created_at,
        )
        for record in history
    ]
