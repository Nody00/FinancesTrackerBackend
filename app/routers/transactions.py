from database import get_db
from models import Transaction
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from utils import get_current_user
from sqlalchemy import and_
from schemas import TransactionCreate, TransactionUpdate
import logging
from datetime import date

# Transactions
# GET /api/transactions - List transactions with optional filters
# POST /api/transactions - Create a new transaction
# PUT /api/transactions/{id} - Update a transaction
# DELETE /api/transactions/{id} - Delete a transaction

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=200)
async def get(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int | None = None,
    limit: int | None = None,
    user_id: int | None = None,
    amount: float | None = None,
    date: date | None = None,
    category_id: int | None = None,
    description: str | None = None,
    type: str | None = None,
    created_at: date | None = None,
    id: int | None = None,
):
    filters = []

    if id is not None:
        filters.append(Transaction.id == id)
    if created_at is not None:
        filters.append(Transaction.created_at == created_at)
    if type is not None:
        filters.append(Transaction.type == type)
    if description is not None:
        filters.append(Transaction.description.ilike(f"%{description}%"))
    if category_id is not None:
        filters.append(Transaction.category_id == category_id)
    if date is not None:
        filters.append(Transaction.date == date)
    if amount is not None:
        filters.append(Transaction.amount == amount)
    if user_id is not None:
        filters.append(Transaction.user_id == user_id)

    query = db.query(Transaction)
    if filters:
        query.filter(and_(*filters))

    if skip is not None:
        query = query.offset(skip)

    if limit is not None:
        query = query.limit(limit)

    transactions = query.all()
    return transactions


@router.post("/", status_code=201)
async def create(
    payload: TransactionCreate, user: user_dependency, db: Session = Depends(get_db)
):
    db_transaction = Transaction(*payload, user_id=user.get("id"))
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@router.patch("/{id}", status_code=204)
async def update(
    id: int,
    payload: TransactionUpdate,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    found_transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not found_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found!")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(found_transaction, field, value)

    db.add(found_transaction)
    db.commit()
    return


@router.delete("/{id}", status_code=200)
async def delete(id: int, user: user_dependency, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if db_transaction.user_id != user.get("id"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this")

    db.delete(db_transaction)
    db.commit()
    return {"message": f"Transaction {id} deleted!"}
