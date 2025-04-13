from fastapi import APIRouter

router = APIRouter()

from . import auth

router.include_router(auth.router, tags=["Auth"])
