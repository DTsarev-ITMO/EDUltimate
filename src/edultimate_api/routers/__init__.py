from .user import router as user_router
from .food import router as food_router
from .vitals import router as vitals_router

routers = [
    user_router,
    food_router,
    vitals_router
]


__all__ = [
    "user_router", "food_router", "vitals_router"
]