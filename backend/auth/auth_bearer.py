import os
from typing import Optional

from auth.api_key_handler import get_user_from_api_key, verify_api_key
from auth.jwt_token_handler import decode_access_token, verify_token
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.users import User


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
    ):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        self.check_scheme(credentials)
        token = credentials.credentials
        return await self.authenticate(
            token,
        )

    def check_scheme(self, credentials):
        if credentials and credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Token must be Bearer")
        elif not credentials:
            raise HTTPException(
                status_code=403, detail="Authentication credentials missing"
            )

    async def authenticate(
        self,
        token: str,
    ):
        if os.environ.get("AUTHENTICATE") == "false":
            return self.get_test_user()
        elif verify_token(token):
            return decode_access_token(token)
        elif await verify_api_key(
            token,
        ):
            return await get_user_from_api_key(
                token,
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid token or api key.")

    def get_test_user(self):
        return {"email": "test@example.com"}  # replace with test user information


def get_current_user(credentials: dict = Depends(AuthBearer())) -> User:
    return User(email=credentials.get("email", "none"))
