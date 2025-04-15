from database import get_db
from models import Category

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from utils import get_current_user
from sqlalchemy import and_
from schemas import CategoryCreate
import logging

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

# Categories
# GET /api/categories - List all categories
# POST /api/categories - Create a new category
# DELETE /api/categories/{id} - Delete a category


@router.get("/")
async def get(
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


@router.post("/", status_code=201)
async def create(
    payload: CategoryCreate, user: user_dependency, db: Session = Depends(get_db)
):
    db_category = Category(name=payload.name, user_id=user.get("id"))
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{id}", status_code=200)
async def delete(id: int, user: user_dependency, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == id).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if db_category.user_id != user.get("id"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this")

    db.delete(db_category)
    db.commit()
    return {"message": f"Category {id} deleted!"}
