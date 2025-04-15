from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import HTTPException
from routers import auth
import logging
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    logging.warning(token)
    payload = jwt.decode(jwt=token, key=auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    logging.warning(payload)

    if not payload["userData"]:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["userData"]["id"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"user": user}
