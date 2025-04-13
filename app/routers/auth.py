from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt


router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=201)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user.

    - Hashes the user's password.
    - Creates a new user in the database.
    - Returns the newly created user
    """
    try:
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode()
        db_user = User(
            username=user.username, email=user.email, password_hash=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "username": db_user.username,
            "created_at": db_user.created_at,
            "id": db_user.id,
            "email": db_user.email,
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists!")
    finally:
        db.close()
