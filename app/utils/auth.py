from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import jwt
from routers import auth
import logging
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    logging.warning(token)
    payload = jwt.decode(jwt=token, key=auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    logging.warning(payload)
    #     {'userData': {'id': 15, 'email': 'shiredude@gmail.com', 'created_at': 1744565888.052378, 'username': 'bilboBagins311'}, 'expires_at': 1745310301.156434}
    # WARNING:root:{'user': 'test'}
    # check if user exists in db
    # if so return the user
    # if not throw error
    return {"user": "test"}
