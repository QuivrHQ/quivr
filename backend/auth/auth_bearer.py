from typing import Optional
from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from models.users import User
from utils.vectors import CommonsDep
from asyncpg.exceptions import DataError
from auth.auth_handler import decode_access_token
from datetime import datetime

class JWTBearer(HTTPBearer):
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

    async def authenticate(self, token, commons):
        if os.environ.get("AUTHENTICATE") == "false":
            return self.get_test_user()
        elif self.verify_jwt(token):
            return self.decode_jwt(token)
        elif await self.verify_api_key(token, commons):
            return await self.get_user_from_api_key(token, commons)
        else:
            raise HTTPException(status_code=402, detail="Invalid token or expired token.")

    def get_test_user(self):
        return {'email': 'test@example.com'}  # replace with test user information

    def verify_jwt(self, jwtoken: str):
        payload = decode_access_token(jwtoken)
        return payload is not None

    def decode_jwt(self, jwtoken: str):
        return decode_access_token(jwtoken)

    async def verify_api_key(self, api_key: str, commons: CommonsDep):
        try:
            # Use UTC time to avoid timezone issues
            current_date = datetime.utcnow().date()
            result = commons['supabase'].table('api_keys').select('api_key', 'creation_time').filter('api_key', 'eq', api_key).filter('is_active', 'eq', True).execute()
            if result.data is not None and len(result.data) > 0:
                api_key_creation_date = datetime.strptime(result.data[0]['creation_time'], "%Y-%m-%dT%H:%M:%S").date()

                # Check if the API key was created today: Todo remove this check and use deleted_time instead.
                if api_key_creation_date == current_date:
                    return True
            return False
        except DataError:
            return False


    async def get_user_from_api_key(self, api_key: str, commons: CommonsDep):
    # Lookup the user_id from the api_keys table
        user_id_data = commons['supabase'].table('api_keys').select('user_id').filter('api_key', 'eq', api_key).execute()
    
        if not user_id_data.data:
            raise HTTPException(status_code=400, detail="Invalid API key.")
    
        user_id = user_id_data.data[0]['user_id']

        # Lookup the email from the users table. Todo: remove and use user_id for credentials
        user_email_data = commons['supabase'].table('users').select('email').filter('user_id', 'eq', user_id).execute()

        return {'email': user_email_data.data[0]['email']} if user_email_data.data else {'email': None}



def get_current_user(credentials: dict = Depends(JWTBearer())) -> User:
    return User(email=credentials.get('email', 'none'))
