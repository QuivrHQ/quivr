import os

from auth.api_key_handler import verify_api_key, get_user_from_api_key
from auth.jwt_token_handler import decode_access_token, verify_token

from typing import Optional
from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.users import User
from utils.vectors import CommonsDep

class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, commons: CommonsDep):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        self.check_scheme(credentials)
        token = credentials.credentials
        return await self.authenticate(token, commons)

    def check_scheme(self, credentials):
        if credentials and not credentials.scheme == "Bearer":
            raise HTTPException(status_code=402, detail="Invalid authorization scheme.")
        elif not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def authenticate(self, token: str, commons: CommonsDep):
        if os.environ.get("AUTHENTICATE") == "false":
            return self.get_test_user()
        elif verify_token(token):
            return decode_access_token(token)
        elif await verify_api_key(token, commons):
            return await get_user_from_api_key(token, commons)
        else:
            raise HTTPException(status_code=402, detail="Invalid token or expired token.")

    def get_test_user(self):
        return {'email': 'test@example.com'}  # replace with test user information

def get_current_user(credentials: dict = Depends(AuthBearer())) -> User:
    return User(email=credentials.get('email', 'none'))
