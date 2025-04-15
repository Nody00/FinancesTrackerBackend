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
    user_id: int


class TransactionCreate(TransactionBase):

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 23.232,
                "date": "01/02/2000",
                "category_id": 1,
                "description": "Test description",
                "type": "income",
                "user_id": 1,
            }
        }


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
