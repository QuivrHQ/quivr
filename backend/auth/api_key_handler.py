
from datetime import datetime
from fastapi import HTTPException

from pydantic import DateError
from utils.vectors import CommonsDep


async def verify_api_key(api_key: str, commons: CommonsDep):     
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
    except DateError:
        return False
    
async def get_user_from_api_key(api_key: str, commons: CommonsDep):
    # Lookup the user_id from the api_keys table
        user_id_data = commons['supabase'].table('api_keys').select('user_id').filter('api_key', 'eq', api_key).execute()
    
        if not user_id_data.data:
            raise HTTPException(status_code=400, detail="Invalid API key.")
    
        user_id = user_id_data.data[0]['user_id']

        # Lookup the email from the users table. Todo: remove and use user_id for credentials
        user_email_data = commons['supabase'].table('users').select('email').filter('user_id', 'eq', user_id).execute()

        return {'email': user_email_data.data[0]['email']} if user_email_data.data else {'email': None}
