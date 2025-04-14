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

# some fake data
SECRET_KEY = "6391e4f3bd7800d4b24a02cc0f077fccd2d1ab65b483371a0ccf3f4d0f91415a5da47a6753c5bacec87ea5e9547c1ff980c7f2f50dd4bfc5a2ea64e238623399d4cd3e6cdf2d398d638f26e62ea22ecbc2f7c1d7abfe0923639911202ed7bcfb43a51bc1e6f5159b4ecdb55a8c81c3606eb9e9ed410b865f21c5b14fab50bd3f9f89e90de97790f2eb1a361a9f254135d3f264835126252b4ea62be51813d972fa7acb72ce92554a7f9ff04fa15858f6ceca6f083b14d373d34e818443d647ed898d9fdd2029ce19db5b7586196be37f0f1380369b3a9560c86aca068f1e1267d861a8d59aa6292dfadb36add56f7cd27cd0b8262e340bcaf88c6d4cfadcc905"
ALGORITHM = "HS256"


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


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(payload: UserLoginPayload, db: Session = Depends(get_db)):
    """
    Endpoint for logging in.
    - Receives email and password
    - Checks if such user exists
    - Return a jwt token along with user data
    """

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email or password are invalid")

    is_password_valid = bcrypt.checkpw(
        payload.password.encode("utf-8"), user.password_hash.encode("utf-8")
    )

    if not is_password_valid:
        raise HTTPException(status_code=404, detail="Email or password are invalid")

    serialized_user = {
        "id": user.id,
        "email": user.email,
        "created_at": datetime.timestamp(user.created_at),
        "username": user.username,
    }

    timestamp = datetime.now(tz=None) + timedelta(days=7)
    float_timestamp = timestamp.timestamp()

    jwt_payload = {"userData": serialized_user, "expires_at": float_timestamp}

    encoded_payload = jwt.encode(jwt_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"token": encoded_payload, "user": serialized_user}
