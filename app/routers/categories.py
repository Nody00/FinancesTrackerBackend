from database import get_db
from models import User, Category
from schemas import UserCreate, UserResponse, UserLoginPayload, LoginResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Annotated
from utils import get_current_user
from sqlalchemy import and_, or_
import logging

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

# Categories
# GET /api/categories - List all categories
# POST /api/categories - Create a new category
# DELETE /api/categories/{id} - Delete a category


@router.get("/")
async def get_categories(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int | None = None,
    limit: int | None = None,
    id: int | None = None,
    name: str | None = None,
    user_id: int | None = None,
):
    filters = []

    if id is not None:
        filters.append(Category.id == id)
    if name is not None:
        filters.append(Category.name.ilike(f"%{name}%"))
    if user_id is not None:
        filters.append(Category.user_id == user_id)

    query = db.query(Category)
    if filters:
        query.filter(and_(*filters))

    if skip is not None:
        query = query.offset(skip)

    if limit is not None:
        query = query.limit(limit)

    categories = query.all()
    return categories
