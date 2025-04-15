from fastapi import APIRouter

router = APIRouter()

from . import auth, categories, transactions


router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(categories.router, prefix="/categories", tags=["Categories"])
router.include_router(
    transactions.router, prefix="/transactions", tags=["Transactions"]
)
