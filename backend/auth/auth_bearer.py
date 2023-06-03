import os
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth_handler import decode_access_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if os.environ.get("AUTHENTICATE") == "false":
            return True
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=402, detail="Invalid authorization scheme.")
            token = credentials.credentials
            if not self.verify_jwt(token):
                raise HTTPException(status_code=402, detail="Invalid token or expired token.")
            return self.verify_jwt(token)  # change this line
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str):
        payload = decode_access_token(jwtoken)
        return payload