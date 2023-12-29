import os

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

load_dotenv()
security = HTTPBearer()

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(authorization: HTTPAuthorizationCredentials = Security(security)):
    token = authorization.credentials
    try:
        payload = jwt.decode(token, os.getenv("SECRET"), algorithms=[os.getenv("ALGORITHM")])
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        return user_id
    except PyJWTError:
        raise credentials_exception
