import fastapi

from src.api.routes.authentication import router as auth_router
from src.api.routes.balance import router as balance_router
from src.api.routes.character import router as character_router
from src.api.routes.item import router as item_router
from src.api.routes.user import router as user_router

router = fastapi.APIRouter()

router.include_router(router=auth_router)
router.include_router(router=balance_router)
router.include_router(router=character_router)
router.include_router(router=item_router)
router.include_router(router=user_router)
