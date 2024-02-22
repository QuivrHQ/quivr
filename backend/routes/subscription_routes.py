from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from middlewares.auth.auth_bearer import AuthBearer, get_current_user
from models import BrainSubscription
from modules.brain.entity.brain_entity import RoleEnum
from modules.brain.service.api_brain_definition_service import ApiBrainDefinitionService
from modules.brain.service.brain_authorization_service import (
    has_brain_authorization,
    validate_brain_authorization,
)
from modules.brain.service.brain_service import BrainService
from modules.brain.service.brain_user_service import BrainUserService
from modules.prompt.entity.prompt import PromptStatusEnum
from modules.prompt.service.prompt_service import PromptService
from modules.user.entity.user_identity import UserIdentity
from modules.user.service.user_service import UserService
from pydantic import BaseModel
from repository.brain_subscription import (
    SubscriptionInvitationService,
    resend_invitation_email,
)
from routes.headers.get_origin_header import get_origin_header

subscription_router = APIRouter()
subscription_service = SubscriptionInvitationService()
user_service = UserService()
prompt_service = PromptService()
brain_user_service = BrainUserService()
brain_service = BrainService()
api_brain_definition_service = ApiBrainDefinitionService()


@subscription_router.post(
    "/brains/{brain_id}/subscription",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
        Depends(has_brain_authorization([RoleEnum.Owner, RoleEnum.Editor])),
        Depends(get_origin_header),
    ],
    tags=["BrainSubscription"],
)
def invite_users_to_brain(
    brain_id: UUID,
    users: List[dict],
    origin: str = Depends(get_origin_header),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Invite multiple users to a brain by their emails. This function creates
    or updates a brain subscription invitation for each user and sends an
    invitation email to each user.
    """
    for user in users:
        subscription = BrainSubscription(
            brain_id=brain_id, email=user["email"], rights=user["rights"]
        )
        # check if user is an editor but trying to give high level permissions
        if subscription.rights == "Owner":
            try:
                validate_brain_authorization(
                    brain_id,
                    current_user.id,
                    RoleEnum.Owner,
                )
            except HTTPException:
                raise HTTPException(
                    status_code=403,
                    detail="You don't have the rights to give owner permissions",
                )

        try:
            should_send_invitation_email = (
                subscription_service.create_or_update_subscription_invitation(
                    subscription
                )
            )
            if should_send_invitation_email:
                resend_invitation_email(
                    subscription,
                    inviter_email=current_user.email or "Quivr",
                    user_id=current_user.id,
                    origin=origin,
                )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error inviting user: {e}")

    return {"message": "Invitations sent successfully"}


@subscription_router.get(
    "/brains/{brain_id}/users",
    dependencies=[
        Depends(AuthBearer()),
        Depends(has_brain_authorization([RoleEnum.Owner, RoleEnum.Editor])),
    ],
)
def get_users_with_brain_access(
    brain_id: UUID,
):
    """
    Get all users for a brain
    """

    brain_users = brain_user_service.get_brain_users(
        brain_id=brain_id,
    )

    brain_access_list = []

    for brain_user in brain_users:
        brain_access = {}
        # TODO: find a way to fetch user email concurrently
        brain_access["email"] = user_service.get_user_email_by_user_id(
            brain_user.user_id
        )
        brain_access["rights"] = brain_user.rights
        brain_access_list.append(brain_access)

    return brain_access_list


@subscription_router.delete(
    "/brains/{brain_id}/subscription",
)
async def remove_user_subscription(
    brain_id: UUID, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Remove a user's subscription to a brain
    """
    targeted_brain = brain_service.get_brain_by_id(brain_id)

    if targeted_brain is None:
        raise HTTPException(
            status_code=404,
            detail="Brain not found while trying to delete",
        )

    user_brain = brain_user_service.get_brain_for_user(current_user.id, brain_id)
    if user_brain is None:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission for this brain",
        )

    if user_brain.rights != "Owner":
        brain_user_service.delete_brain_user(current_user.id, brain_id)
    else:
        brain_users = brain_user_service.get_brain_users(
            brain_id=brain_id,
        )
        brain_other_owners = [
            brain
            for brain in brain_users
            if brain.rights == "Owner" and str(brain.user_id) != str(current_user.id)
        ]

        if len(brain_other_owners) == 0:
            brain_service.delete_brain(
                brain_id=brain_id,
            )
            if targeted_brain.prompt_id:
                brain_to_delete_prompt = prompt_service.get_prompt_by_id(
                    targeted_brain.prompt_id
                )
                if brain_to_delete_prompt is not None and (
                    brain_to_delete_prompt.status == PromptStatusEnum.private
                ):
                    prompt_service.delete_prompt_by_id(targeted_brain.prompt_id)

        else:
            brain_user_service.delete_brain_user(
                current_user.id,
                brain_id,
            )

    return {"message": f"Subscription removed successfully from brain {brain_id}"}


@subscription_router.get(
    "/brains/{brain_id}/subscription",
    dependencies=[Depends(AuthBearer())],
    tags=["BrainSubscription"],
)
def get_user_invitation(
    brain_id: UUID, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Get an invitation to a brain for a user. This function checks if the user
    has been invited to the brain and returns the invitation status.
    """
    if not current_user.email:
        raise HTTPException(status_code=400, detail="UserIdentity email is not defined")

    subscription = BrainSubscription(brain_id=brain_id, email=current_user.email)

    invitation = subscription_service.fetch_invitation(subscription)

    if invitation is None:
        raise HTTPException(
            status_code=404,
            detail="You have not been invited to this brain",
        )

    brain_details = brain_service.get_brain_details(brain_id, current_user.id)

    if brain_details is None:
        raise HTTPException(
            status_code=404,
            detail="Brain not found while trying to get invitation",
        )

    return {"name": brain_details.name, "rights": invitation["rights"]}


@subscription_router.post(
    "/brains/{brain_id}/subscription/accept",
    tags=["Brain"],
)
async def accept_invitation(
    brain_id: UUID, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Accept an invitation to a brain for a user. This function removes the
    invitation from the subscription invitations and adds the user to the
    brain users.
    """
    if not current_user.email:
        raise HTTPException(status_code=400, detail="UserIdentity email is not defined")

    subscription = BrainSubscription(brain_id=brain_id, email=current_user.email)

    try:
        invitation = subscription_service.fetch_invitation(subscription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching invitation: {e}")

    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    try:
        brain_user_service.create_brain_user(
            user_id=current_user.id,
            brain_id=brain_id,
            rights=invitation["rights"],
            is_default_brain=False,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding user to brain: {e}")

    try:
        subscription_service.remove_invitation(subscription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error removing invitation: {e}")

    return {"message": "Invitation accepted successfully"}


@subscription_router.post(
    "/brains/{brain_id}/subscription/decline",
    tags=["Brain"],
)
async def decline_invitation(
    brain_id: UUID, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Decline an invitation to a brain for a user. This function removes the
    invitation from the subscription invitations.
    """
    if not current_user.email:
        raise HTTPException(status_code=400, detail="UserIdentity email is not defined")

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


class BrainSubscriptionUpdatableProperties(BaseModel):
    rights: str | None = None
    email: str


@subscription_router.put(
    "/brains/{brain_id}/subscription",
    dependencies=[
        Depends(AuthBearer()),
        Depends(has_brain_authorization([RoleEnum.Owner, RoleEnum.Editor])),
    ],
)
def update_brain_subscription(
    brain_id: UUID,
    subscription: BrainSubscriptionUpdatableProperties,
    current_user: UserIdentity = Depends(get_current_user),
):
    user_email = subscription.email
    if user_email == current_user.email:
        raise HTTPException(
            status_code=403,
            detail="You can't change your own permissions",
        )

    user_id = user_service.get_user_id_by_email(user_email)

    if user_id is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # check if user is an editor but trying to give high level permissions
    if subscription.rights == "Owner":
        try:
            validate_brain_authorization(
                brain_id,
                current_user.id,
                RoleEnum.Owner,
            )
        except HTTPException:
            raise HTTPException(
                status_code=403,
                detail="You don't have the rights to give owner permissions",
            )

    # check if user is not an editor trying to update an owner right which is not allowed
    current_invitation = brain_user_service.get_brain_for_user(user_id, brain_id)
    if current_invitation is not None and current_invitation.rights == "Owner":
        try:
            validate_brain_authorization(
                brain_id,
                current_user.id,
                RoleEnum.Owner,
            )
        except HTTPException:
            raise HTTPException(
                status_code=403,
                detail="You can't change the permissions of an owner",
            )

    # removing user access from brain
    if subscription.rights is None:
        try:
            # only owners can remove user access to a brain
            validate_brain_authorization(
                brain_id,
                current_user.id,
                RoleEnum.Owner,
            )
            brain_user_service.delete_brain_user(user_id, brain_id)
        except HTTPException:
            raise HTTPException(
                status_code=403,
                detail="You don't have the rights to remove user access",
            )
    else:
        brain_user_service.update_brain_user_rights(
            brain_id, user_id, subscription.rights
        )

    return {"message": "Brain subscription updated successfully"}


@subscription_router.post(
    "/brains/{brain_id}/subscribe",
    tags=["Subscription"],
)
async def subscribe_to_brain_handler(
    brain_id: UUID,
    secrets: dict = {},
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Subscribe to a public brain
    """
    if not current_user.email:
        raise HTTPException(status_code=400, detail="UserIdentity email is not defined")

    brain = brain_service.get_brain_by_id(brain_id)

    if brain is None:
        raise HTTPException(status_code=404, detail="Brain not found")
    if brain.status != "public":
        raise HTTPException(
            status_code=403,
            detail="You cannot subscribe to this brain without invitation",
        )
    # check if user is already subscribed to brain
    user_brain = brain_user_service.get_brain_for_user(current_user.id, brain_id)
    if user_brain is not None:
        raise HTTPException(
            status_code=403,
            detail="You are already subscribed to this brain",
        )
    if brain.brain_type == "api":
        brain_definition = api_brain_definition_service.get_api_brain_definition(
            brain_id
        )
        brain_secrets = brain_definition.secrets if brain_definition != None else []

        for secret in brain_secrets:
            if not secrets[secret.name]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Please provide the secret {secret}",
                )

        for secret in brain_secrets:
            brain_service.external_api_secrets_repository.create_secret(
                user_id=current_user.id,
                brain_id=brain_id,
                secret_name=secret.name,
                secret_value=secrets[secret.name],
            )

    try:
        brain_user_service.create_brain_user(
            user_id=current_user.id,
            brain_id=brain_id,
            rights=RoleEnum.Viewer,
            is_default_brain=False,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding user to brain: {e}")

    return {"message": "You have successfully subscribed to the brain"}


@subscription_router.post(
    "/brains/{brain_id}/unsubscribe",
    tags=["Subscription"],
)
async def unsubscribe_from_brain_handler(
    brain_id: UUID, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Unsubscribe from a brain
    """
    if not current_user.email:
        raise HTTPException(status_code=400, detail="UserIdentity email is not defined")

    brain = brain_service.get_brain_by_id(brain_id)

    if brain is None:
        raise HTTPException(status_code=404, detail="Brain not found")
    if brain.status != "public":
        raise HTTPException(
            status_code=403,
            detail="You cannot subscribe to this brain without invitation",
        )
    # check if user is already subscribed to brain
    user_brain = brain_user_service.get_brain_for_user(current_user.id, brain_id)
    if user_brain is None:
        raise HTTPException(
            status_code=403,
            detail="You are not subscribed to this brain",
        )
    brain_user_service.delete_brain_user(user_id=current_user.id, brain_id=brain_id)

    return {"message": "You have successfully unsubscribed from the brain"}
