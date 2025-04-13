from typing import Optional
from decimal import Decimal

from pydantic import BaseModel


class BudgetBase(BaseModel):
    category_id: int
    amount: Decimal
    month: int
    year: int


class BudgetCreate(BudgetBase):
    user_id: int  # Or get from token


class BudgetUpdate(BudgetBase):
    amount: Optional[Decimal] = None


class Budget(BudgetBase):
    id: int
    user_id: int
