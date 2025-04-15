from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserLoginPayload, LoginResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
import jwt
from datetime import datetime, timedelta


router = APIRouter()


# Categories
# GET /api/categories - List all categories
# POST /api/categories - Create a new category
# DELETE /api/categories/{id} - Delete a category


@router.get("/")
async def get_categories():
    return {"message": "nothing"}
