import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET
from app.database.db import get_db
from app.user.user_model import User

security = HTTPBearer()

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(authorization: HTTPAuthorizationCredentials = Security(security)):
    """Return the authenticated user's id (their e-mail), decoded from the JWT.

    ``algorithms`` is a single-element allow-list and the claims are required
    rather than merely read. Both matter: a decoder that accepts whatever
    algorithm the token's own header names is the classic JWT forgery, and a
    token without ``exp`` never expires.
    """
    token = authorization.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"], "verify_exp": True},
        )
        user_id = payload.get("sub")

        if not user_id:
            raise credentials_exception
        return user_id
    except PyJWTError as exc:
        raise credentials_exception from exc


def get_current_user_record(
    userid: str = Depends(get_current_user), db: Session = Depends(get_db)
) -> User:
    """Return the authenticated user's row.

    Statements are keyed by display name (``from_user`` / ``to_user``), not by
    userid, so routes that need to scope data to the caller resolve the full
    record rather than just the token subject.
    """
    user = db.query(User).filter(User.userid == userid).first()
    if user is None:
        raise credentials_exception
    return user
