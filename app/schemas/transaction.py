from typing import Optional
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    amount: Decimal
    date: date
    category_id: Optional[int] = None
    description: Optional[str] = None
    type: str  # 'income' or 'expense'


class TransactionCreate(TransactionBase):
    user_id: int  # Or get from token


class TransactionUpdate(TransactionBase):
    amount: Optional[Decimal] = None
    date: Optional[date] = None  # type: ignore
    category_id: Optional[int] = None
    description: Optional[str] = None
    type: Optional[str] = None


class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
