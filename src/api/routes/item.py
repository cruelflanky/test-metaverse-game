from uuid import UUID

import fastapi

from src.crud.item import ItemCRUDInterface, ItemTransferHistoryCRUDInterface
from src.crud.base import get_interface
from src.schemas.routes.item import ItemCreateType, ItemEquipType, ItemType, ItemTransferHistoryType, ItemTransferType

router = fastapi.APIRouter(prefix="/items", tags=["items"])


@router.post(
    path="",
    name="items:create-item",
    response_model=ItemType,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_item(
    item_create: ItemCreateType,
    item_interface: ItemCRUDInterface = fastapi.Depends(get_interface(interface_type=ItemCRUDInterface)),
) -> ItemType:
    new_item = await item_interface.create_item(item_create=item_create)
    return ItemType(
        id=new_item.id,
        type_id=new_item.type_id,
        character_id=new_item.character_id,
        owner_id=new_item.owner_id,
        is_equipped=new_item.is_equipped,
    )


@router.patch(
    path="/equip",
    name="items:equip-item",
    response_model=ItemType,
    status_code=fastapi.status.HTTP_200_OK,
)
async def equip_item(
    item_equip: ItemEquipType,
    item_interface: ItemCRUDInterface = fastapi.Depends(get_interface(interface_type=ItemCRUDInterface)),
) -> ItemType:
    updated_item = await item_interface.equip_item(item_equip=item_equip)
    return ItemType(
        id=updated_item.id,
        type_id=updated_item.type_id,
        character_id=updated_item.character_id,
        owner_id=updated_item.owner_id,
        is_equipped=updated_item.is_equipped,
    )


@router.post(
    path="/transfer",
    name="items:transfer-item",
    response_model=ItemTransferHistoryType,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def transfer_item(
    item_transfer: ItemTransferType,
    item_transfer_interface: ItemTransferHistoryCRUDInterface = fastapi.Depends(
        get_interface(interface_type=ItemTransferHistoryCRUDInterface)
    ),
) -> ItemTransferHistoryType:
    transfer_history = await item_transfer_interface.transfer_item(item_transfer=item_transfer)
    return ItemTransferHistoryType(
        id=transfer_history.id,
        item_id=transfer_history.item_id,
        from_owner_id=transfer_history.from_owner_id,
        to_owner_id=transfer_history.to_owner_id,
        fee_amount=transfer_history.fee_amount,
        balance_transfer_history_id=transfer_history.balance_transfer_history_id,
        created_at=transfer_history.created_at,
    )
