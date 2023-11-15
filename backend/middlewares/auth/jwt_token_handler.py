import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from jose.exceptions import JWTError
from modules.user.entity.user_identity import UserIdentity

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> UserIdentity:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False}
        )
    except JWTError:
        return None  # pyright: ignore reportPrivateUsage=none

    return UserIdentity(
        email=payload.get("email"),
        id=payload.get("sub"),  # pyright: ignore reportPrivateUsage=none
    )


def verify_token(token: str):
    payload = decode_access_token(token)
    return payload is not None
