from fastapi import APIRouter

router = APIRouter()

from . import auth, categories


router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(categories.router, prefix="/categories", tags=["Categories"])
