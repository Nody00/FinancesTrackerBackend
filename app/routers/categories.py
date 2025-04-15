from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserLoginPayload, LoginResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Annotated
from utils import get_current_user
import logging

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

# Categories
# GET /api/categories - List all categories
# POST /api/categories - Create a new category
# DELETE /api/categories/{id} - Delete a category


@router.get("/")
async def get_categories(user: user_dependency):
    logging.warning(user)
    return {"message": "nothing"}
