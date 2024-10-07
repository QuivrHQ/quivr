from uuid import uuid4

import pytest_asyncio
from quivr_api.modules.user.entity.user_identity import User
from sqlmodel import select, text
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def other_user(session: AsyncSession):
    sql = text(
        """
        INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at") VALUES
        ('00000000-0000-0000-0000-000000000000', :id , 'authenticated', 'authenticated', 'other@quivr.app', '$2a$10$vwKX0eMLlrOZvxQEA3Vl4e5V4/hOuxPjGYn9QK1yqeaZxa.42Uhze', '2024-01-22 22:27:00.166861+00', NULL, '', NULL, 'e91d41043ca2c83c3be5a6ee7a4abc8a4f4fb1afc0a8453c502af931', '2024-03-05 16:22:13.780421+00', '', '', NULL, '2024-03-30 23:21:12.077887+00', '{"provider": "email", "providers": ["email"]}', '{}', NULL, '2024-01-22 22:27:00.158026+00', '2024-04-01 17:40:15.332205+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL);
        """
    )
    await session.execute(sql, params={"id": uuid4()})

    other_user = (
        await session.exec(select(User).where(User.email == "other@quivr.app"))
    ).one()
    return other_user
