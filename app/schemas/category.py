from typing import Optional, List

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    user_id: int  # Or consider excluding this and getting it from the token


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    icon: Optional[str] = None


class Category(CategoryBase):
    id: int
    user_id: int


class CategoryWithRelations(Category):
    transactions: Optional[List["Transaction"]] = None
    budgets: Optional[List["Budget"]] = None


from .transaction import Transaction
from .budget import Budget

CategoryWithRelations.update_forward_refs()
