from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    password: str = Field(
        min_length=8, description="Password must be a minimum of 8 characters"
    )
    username: str = Field(
        min_length=5, description="Username must be a minimum of 5 characters long"
    )
    email: EmailStr

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
    email: EmailStr


class UserLoginPayload(BaseModel):
    username: str
    password: str = Field(
        min_length=8, description="Password must be a minimum of 8 characters"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "bilboBagins311",
                "password": "theonering",
            }
        }


class UserInfo(BaseModel):
    id: int
    email: str
    created_at: float
    username: str


class LoginResponse(BaseModel):
    token: str
