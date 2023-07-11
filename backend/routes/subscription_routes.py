from typing import List
from uuid import UUID

from auth.auth_bearer import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from models.brains_subscription_invitations import BrainSubscription
from models.users import User

subscription_router = APIRouter()


@subscription_router.post("/brain/{brain_id}/subscription")
async def invite_user_to_brain(brain_id: UUID, users: List[dict], current_user: User = Depends(get_current_user)):
    # TODO: Ensure the current user has permissions to invite users to this brain
    
    for user in users:
        subscription = BrainSubscription(brain_id=brain_id, email=user['email'], rights=user['rights'], inviter_email=current_user.email or "Quivr")
        
        try:
            subscription.create_or_update_subscription_invitation()
            subscription.resend_invitation_email()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error inviting user: {e}")

    return {"message": "Invitations sent successfully"}
