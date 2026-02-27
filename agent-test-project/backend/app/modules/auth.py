import logging
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.config import CONFIG

logger = logging.getLogger(__name__)

security = HTTPBearer()


class LoginRequest(BaseModel):
    password: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES()
    )
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, CONFIG.JWT_SECRET(), algorithm=CONFIG.JWT_ALGORITHM()
    )
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, CONFIG.JWT_SECRET(), algorithms=[CONFIG.JWT_ALGORITHM()]
        )
        return payload
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
