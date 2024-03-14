from typing import Optional

from pydantic import BaseModel


class UserUpdatableProperties(BaseModel):
    # Nothing for now
    username: Optional[str] = None
    company: Optional[str] = None
    onboarded: Optional[bool] = None
    company_size: Optional[str] = None
    role_in_company: Optional[str] = None

