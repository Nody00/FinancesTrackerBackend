from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "bilboBagins311",
                "email": "shiredude@gmail.com",
                "password": "theonering",
            }
        }


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    email: str
