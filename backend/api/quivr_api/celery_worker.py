import os
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from uuid import UUID

from celery.schedules import crontab
from pytz import timezone

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth.auth_bearer import AuthBearer
from quivr_api.models.files import File
from quivr_api.models.settings import get_supabase_client, get_supabase_db
from quivr_api.modules.brain.integrations.Notion.Notion_connector import NotionConnector
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.packages.files.crawl.crawler import CrawlWebsite, slugify
from quivr_api.packages.files.processors import filter_file
from quivr_api.packages.utils.telemetry import maybe_send_telemetry

logger = get_logger(__name__)

notification_service = NotificationService()
brain_service = BrainService()
auth_bearer = AuthBearer()


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_file_and_notify",
    autoretry_for=(Exception,),
)
def process_file_and_notify(
    file_name: str,
    file_original_name: str,
    brain_id,
    notification_id: UUID,
    knowledge_id: UUID,
    integration=None,
    integration_link=None,
    delete_file=False,
):
    logger.debug(
        f"process_file file_name={file_name}, knowledge_id={knowledge_id}, brain_id={brain_id}, notification_id={notification_id}"
    )
    supabase_client = get_supabase_client()
    tmp_name = file_name.replace("/", "_")
    base_file_name = os.path.basename(file_name)
    _, file_extension = os.path.splitext(base_file_name)

    with NamedTemporaryFile(
        suffix="_" + tmp_name,  # pyright: ignore reportPrivateUsage=none
    ) as tmp_file:
        res = supabase_client.storage.from_("quivr").download(file_name)
        tmp_file.write(res)
        tmp_file.flush()
        file_instance = File(
            file_name=base_file_name,
            tmp_file_path=tmp_file.name,
            bytes_content=res,
            file_size=len(res),
            file_extension=file_extension,
        )
        brain_vector_service = BrainVectorService(brain_id)
        if delete_file:  # TODO fix bug
            brain_vector_service.delete_file_from_brain(
                file_original_name, only_vectors=True
            )

        filter_file(
            file=file_instance,
            brain_id=brain_id,
            original_file_name=file_original_name,
            integration=integration,
            integration_link=integration_link,
        )

        brain_service.update_brain_last_update_time(brain_id)


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_crawl_and_notify",
    autoretry_for=(Exception,),
)
def process_crawl_and_notify(
    crawl_website_url: str,
    brain_id: UUID,
    knowledge_id: UUID,
    notification_id=None,
):
    crawl_website = CrawlWebsite(url=crawl_website_url)
    # Build file data
    extracted_content = crawl_website.process()
    extracted_content_bytes = extracted_content.encode("utf-8")
    file_name = slugify(crawl_website.url) + ".txt"

    with NamedTemporaryFile(
        suffix="_" + file_name,  # pyright: ignore reportPrivateUsage=none
    ) as tmp_file:
        tmp_file.write(extracted_content_bytes)
        tmp_file.flush()
        file_instance = File(
            file_name=file_name,
            tmp_file_path=tmp_file.name,
            bytes_content=extracted_content_bytes,
            file_size=len(extracted_content),
            file_extension=".txt",
        )
        filter_file(
            file=file_instance,
            brain_id=brain_id,
            original_file_name=crawl_website_url,
        )


@celery.task(name="NotionConnectorLoad")
def process_integration_brain_created_initial_load(brain_id, user_id):
    notion_connector = NotionConnector(brain_id=brain_id, user_id=user_id)

    pages = notion_connector.load()

    print("pages: ", len(pages))


@celery.task
def process_integration_brain_sync_user_brain(brain_id, user_id):
    notion_connector = NotionConnector(brain_id=brain_id, user_id=user_id)

    notion_connector.poll()


@celery.task
def ping_telemetry():
    maybe_send_telemetry("ping", {"ping": "pong"})


@celery.task(name="check_if_is_premium_user")
def check_if_is_premium_user():
    if os.getenv("DEACTIVATE_STRIPE") == "true":
        logger.info("Stripe deactivated, skipping check for premium users")
        return True

    supabase = get_supabase_db()
    supabase_db = supabase.db

    paris_tz = timezone("Europe/Paris")
    current_time = datetime.now(paris_tz)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    logger.debug(f"Current time: {current_time_str}")

    # Define the memoization period (e.g., 1 hour)
    memoization_period = timedelta(hours=1)
    memoization_cutoff = current_time - memoization_period

    # Fetch all necessary data in bulk
    subscriptions = (
        supabase_db.table("subscriptions")
        .select("*")
        .filter("current_period_end", "gt", current_time_str)
        .execute()
    ).data

    customers = (supabase_db.table("customers").select("*").execute()).data

    customer_emails = [customer["email"] for customer in customers]

    # Split customer emails into batches of 50
    email_batches = [
        customer_emails[i : i + 20] for i in range(0, len(customer_emails), 20)
    ]

    users = []
    for email_batch in email_batches:
        batch_users = (
            supabase_db.table("users")
            .select("id, email")
            .in_("email", email_batch)
            .execute()
        ).data
        users.extend(batch_users)

    product_features = (
        supabase_db.table("product_to_features").select("*").execute()
    ).data

    user_settings = (supabase_db.table("user_settings").select("*").execute()).data

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
        supabase_db.table("user_settings").upsert(batch).execute()

    # Delete settings for non-premium users in batches of 10
    settings_to_delete = [
        setting["user_id"]
        for setting in user_settings
        if setting["user_id"] not in premium_user_ids and setting.get("is_premium")
    ]
    for i in range(0, len(settings_to_delete), 10):
        batch = settings_to_delete[i : i + 10]
        supabase_db.table("user_settings").delete().in_("user_id", batch).execute()

    logger.info(
        f"Updated {len(settings_to_upsert)} premium users, deleted settings for {len(settings_to_delete)} non-premium users"
    )
    return True


celery.conf.beat_schedule = {
    "ping_telemetry": {
        "task": f"{__name__}.ping_telemetry",
        "schedule": crontab(minute="*/30", hour="*"),
    },
    "process_sync_active": {
        "task": "process_sync_active",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "process_premium_users": {
        "task": "check_if_is_premium_user",
        "schedule": crontab(minute="*/1", hour="*"),
    },
}
