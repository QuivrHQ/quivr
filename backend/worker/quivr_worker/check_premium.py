import os
from datetime import datetime, timedelta

from postgrest.exceptions import APIError
from pytz import timezone
from quivr_api.logger import get_logger

from supabase import Client

logger = get_logger("celery_worker")


# TODO: Remove all this code and use Stripe Webhooks
def check_is_premium(supabase_client: Client):
    if os.getenv("DEACTIVATE_STRIPE") == "true":
        logger.info("Stripe deactivated, skipping check for premium users")
        return True

    paris_tz = timezone("Europe/Paris")
    current_time = datetime.now(paris_tz)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    logger.debug(f"Current time: {current_time_str}")

    # Define the memoization period (e.g., 1 hour)
    memoization_period = timedelta(hours=1)
    memoization_cutoff = current_time - memoization_period

    # Fetch all necessary data in bulk
    try:
        subscriptions = (
            supabase_client.table("subscriptions")
            .select("*")
            .filter("current_period_end", "gt", current_time_str)
            .execute()
        ).data
    except APIError as e:
        logger.error(f"Error fetching subscribtions : {e}")
        return

    customers = (supabase_client.table("customers").select("*").execute()).data

    customer_emails = [customer["email"] for customer in customers]

    # Split customer emails into batches of 50
    email_batches = [
        customer_emails[i : i + 20] for i in range(0, len(customer_emails), 20)
    ]

    users = []
    for email_batch in email_batches:
        batch_users = (
            supabase_client.table("users")
            .select("id, email")
            .in_("email", email_batch)
            .execute()
        ).data
        users.extend(batch_users)

    product_features = (
        supabase_client.table("product_to_features").select("*").execute()
    ).data

    user_settings = (supabase_client.table("user_settings").select("*").execute()).data

    # Create lookup dictionaries for faster access
    user_dict = {user["email"]: user["id"] for user in users}
    customer_dict = {customer["id"]: customer for customer in customers}
    product_dict = {
        product["stripe_product_id"]: product for product in product_features
    }
    settings_dict = {setting["user_id"]: setting for setting in user_settings}

    # Process subscriptions and update user settings
    premium_user_ids = set()
    settings_to_upsert = {}
    for sub in subscriptions:
        logger.info(f"Subscription {sub['id']}")
        if sub["attrs"]["status"] != "active" and sub["attrs"]["status"] != "trialing":
            logger.info(f"Subscription {sub['id']} is not active or trialing")
            continue

        customer = customer_dict.get(sub["customer"])
        if not customer:
            logger.info(f"No customer found for subscription: {sub['customer']}")
            continue

        user_id = user_dict.get(customer["email"])
        if not user_id:
            logger.info(f"No user found for customer: {customer['email']}")
            continue

        current_settings = settings_dict.get(user_id, {})
        last_check = current_settings.get("last_stripe_check")

        # Skip if the user was checked recently
        if last_check and datetime.fromisoformat(last_check) > memoization_cutoff:
            premium_user_ids.add(user_id)
            logger.info(f"User {user_id} was checked recently")
            continue

        user_id = str(user_id)  # Ensure user_id is a string
        premium_user_ids.add(user_id)

        product_id = sub["attrs"]["items"]["data"][0]["plan"]["product"]
        product = product_dict.get(product_id)
        if not product:
            logger.warning(f"No matching product found for subscription: {sub['id']}")
            continue

        settings_to_upsert[user_id] = {
            "user_id": user_id,
            "max_brains": product["max_brains"],
            "max_brain_size": product["max_brain_size"],
            "monthly_chat_credit": product["monthly_chat_credit"],
            "api_access": product["api_access"],
            "is_premium": True,
            "last_stripe_check": current_time_str,
        }
        logger.info(f"Upserting settings for user {user_id}")

    # Bulk upsert premium user settings in batches of 10
    settings_list = list(settings_to_upsert.values())
    logger.info(f"Upserting {len(settings_list)} settings")
    for i in range(0, len(settings_list), 10):
        batch = settings_list[i : i + 10]
        supabase_client.table("user_settings").upsert(batch).execute()

    # Delete settings for non-premium users in batches of 10
    settings_to_delete = [
        setting["user_id"]
        for setting in user_settings
        if setting["user_id"] not in premium_user_ids and setting.get("is_premium")
    ]
    for i in range(0, len(settings_to_delete), 10):
        batch = settings_to_delete[i : i + 10]
        supabase_client.table("user_settings").delete().in_("user_id", batch).execute()

    logger.info(
        f"Updated {len(settings_to_upsert)} premium users, deleted settings for {len(settings_to_delete)} non-premium users"
    )
    return True
