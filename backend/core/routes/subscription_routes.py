import os
from typing import List
from uuid import UUID

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from models.brains import Brain
from models.brains_subscription_invitations import BrainSubscription
from models.users import User
from repository.brain_subscription.email_service import EmailService
from repository.brain_subscription.subscription_invitation_service import \
    SubscriptionInvitationService
from repository.user.get_user_email_by_user_id import get_user_email_by_user_id
from routes.authorizations.brain_authorization import has_brain_authorization

subscription_router = APIRouter()
subscription_service = SubscriptionInvitationService()
email_service = EmailService(os.getenv("RESEND_API_KEY"))


@subscription_router.post(
    "/brain/{brain_id}/subscription",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
        Depends(has_brain_authorization),
    ],
    tags=["BrainSubscription"],
)
def invite_users_to_brain(brain_id: UUID, users: List[dict], current_user: User = Depends(get_current_user)): 
    for user in users:
        subscription = BrainSubscription(brain_id=brain_id, email=user['email'], rights=user['rights'])
        
        try:
            subscription_service.create_or_update_subscription_invitation(subscription)
            email_service.resend_invitation_email(subscription, inviter_email=current_user.email or "Quivr")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error inviting user: {e}")

    return {"message": "Invitations sent successfully"}


@subscription_router.get(
    "/brain/{brain_id}/users",
    dependencies=[Depends(AuthBearer()), Depends(has_brain_authorization())],
)
def get_brain_users(
    brain_id: UUID,
):
    """
    Get all users for a brain
    """
    brain = Brain(
        id=brain_id,
    )
    brain_users = brain.get_brain_users()

    brain_access_list = []

    for brain_user in brain_users:
        brain_access = {}
        # TODO: find a way to fetch user email concurrently
        brain_access["email"] = get_user_email_by_user_id(brain_user["user_id"])
        brain_access["rights"] = brain_user["rights"]
        brain_access_list.append(brain_access)

    return brain_access_list


@subscription_router.delete(
    "/brain/{brain_id}/subscription",
)
async def remove_user_subscription(
    brain_id: UUID, current_user: User = Depends(get_current_user)
):
    """
    Remove a user's subscription to a brain
    """
    brain = Brain(
        id=brain_id,
    )
    user_brain = brain.get_brain_for_user(current_user.id)
    if user_brain is None:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission for this brain",
        )

    if user_brain.get("rights") != "Owner":
        brain.delete_user_from_brain(current_user.id)
    else:
        brain_users = brain.get_brain_users()
        brain_other_owners = [
            brain
            for brain in brain_users
            if brain["rights"] == "Owner"
            and str(brain["user_id"]) != str(current_user.id)
        ]

        if len(brain_other_owners) == 0:
            brain.delete_brain(current_user.id)
        else:
            brain.delete_user_from_brain(current_user.id)

    return {"message": f"Subscription removed successfully from brain {brain_id}"}


@subscription_router.get(
    "/brain/{brain_id}/subscription",
    dependencies=[Depends(AuthBearer())],
    tags=["BrainSubscription"],
)
def get_user_invitation(brain_id: UUID, current_user: User = Depends(get_current_user)):
    if not current_user.email:
        raise HTTPException(status_code=400, detail="User email is not defined")

    subscription = BrainSubscription(brain_id=brain_id, email=current_user.email)

    has_invitation = subscription_service.check_invitation(subscription)
    return {"hasInvitation": has_invitation}

@subscription_router.post(
    "/brain/{brain_id}/subscription/accept",
    tags=["Brain"],
)
async def accept_invitation(brain_id: UUID, current_user: User = Depends(get_current_user)):
    if not current_user.email:
        raise HTTPException(status_code=400, detail="User email is not defined")

    subscription = BrainSubscription(brain_id=brain_id, email=current_user.email)

    try:
        invitation = subscription_service.fetch_invitation(subscription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching invitation: {e}")

    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    try:
        subscription_service.remove_invitation(subscription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error removing invitation: {e}")

    try:
        brain = Brain(id=brain_id)
        brain.create_brain_user(
            user_id=current_user.id, rights=invitation['rights'], default_brain=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding user to brain: {e}")

    return {"message": "Invitation accepted successfully"}

@subscription_router.post(
    "/brain/{brain_id}/subscription/decline",
    tags=["Brain"],
)
async def decline_invitation(brain_id: UUID, current_user: User = Depends(get_current_user)):
    if not current_user.email:
        raise HTTPException(status_code=400, detail="User email is not defined")

    subscription = BrainSubscription(brain_id=brain_id, email=current_user.email)

    try:
        invitation = subscription_service.fetch_invitation(subscription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching invitation: {e}")
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    try:
        subscription_service.remove_invitation(subscription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error removing invitation: {e}")

    return {"message": "Invitation declined successfully"}
