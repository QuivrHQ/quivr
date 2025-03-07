from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserUpdatableProperties(BaseModel):
    # Nothing for now
    username: Optional[str] = None
    company: Optional[str] = None
    onboarded: Optional[bool] = None
    company_size: Optional[str] = None
    usage_purpose: Optional[str] = None


class CreateUserRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    brains: list[str]


class UpdateUserRequest(BaseModel):
    id: UUID
    firstName: str
    lastName: str
    email: str
    brains: list[str]


class ResetPasswordRequest(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
