import os
from datetime import datetime
from tempfile import NamedTemporaryFile
from uuid import UUID

from celery.schedules import crontab
from celery_config import celery
from logger import get_logger
from middlewares.auth.auth_bearer import AuthBearer
from models.files import File
from models.settings import get_supabase_client, get_supabase_db
from modules.brain.integrations.Notion.Notion_connector import NotionConnector
from modules.brain.service.brain_service import BrainService
from modules.brain.service.brain_vector_service import BrainVectorService
from modules.notification.dto.inputs import NotificationUpdatableProperties
from modules.notification.entity.notification import NotificationsStatusEnum
from modules.notification.service.notification_service import NotificationService
from modules.onboarding.service.onboarding_service import OnboardingService
from packages.files.crawl.crawler import CrawlWebsite, slugify
from packages.files.parsers.github import process_github
from packages.files.processors import filter_file
from packages.utils.telemetry import maybe_send_telemetry
from pytz import timezone

logger = get_logger(__name__)

onboardingService = OnboardingService()
notification_service = NotificationService()
brain_service = BrainService()
auth_bearer = AuthBearer()


@celery.task(name="process_file_and_notify")
def process_file_and_notify(
    file_name: str,
    file_original_name: str,
    brain_id,
    notification_id=None,
    integration=None,
    delete_file=False,
):
    try:
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

            message = filter_file(
                file=file_instance,
                brain_id=brain_id,
                original_file_name=file_original_name,
            )

            if notification_id:
                notification_service.update_notification_by_id(
                    notification_id,
                    NotificationUpdatableProperties(
                        status=NotificationsStatusEnum.SUCCESS,
                        description="Your file has been properly uploaded!",
                    ),
                )
            brain_service.update_brain_last_update_time(brain_id)

            return True

    except TimeoutError:
        logger.error("TimeoutError")

    except Exception as e:
        logger.exception(e)
        notification_service.update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.ERROR,
                description=f"An error occurred while processing the file: {e}",
            ),
        )


@celery.task(name="process_crawl_and_notify")
def process_crawl_and_notify(
    crawl_website_url: str,
    brain_id: UUID,
    notification_id=None,
):

    crawl_website = CrawlWebsite(url=crawl_website_url)

    if not crawl_website.checkGithub():
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
            message = filter_file(
                file=file_instance,
                brain_id=brain_id,
                original_file_name=crawl_website_url,
            )
            notification_service.update_notification_by_id(
                notification_id,
                NotificationUpdatableProperties(
                    status=NotificationsStatusEnum.SUCCESS,
                    description="Your URL has been properly crawled!",
                ),
            )
    else:
        message = process_github(
            repo=crawl_website.url,
            brain_id=brain_id,
        )

    if notification_id:
        notification_service.update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.SUCCESS,
                description="Your file has been properly uploaded!",
            ),
        )

    brain_service.update_brain_last_update_time(brain_id)
    return True


@celery.task
def remove_onboarding_more_than_x_days_task():
    onboardingService.remove_onboarding_more_than_x_days(7)


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
    supabase = get_supabase_db()
    supabase_db = supabase.db
    # Get the list of subscription active

    paris_tz = timezone("Europe/Paris")
    paris_time = datetime.now(paris_tz).strftime("%Y-%m-%d %H:%M:%S.%f")
    logger.debug(f"Paris time: {paris_time}")
    subscriptions = (
        supabase_db.table("subscriptions")
        .select("*")
        .filter(
            "current_period_end",
            "gt",
            paris_time,
        )
        .execute()
    ).data
    # Only get the subscriptions with status active
    logger.info(f"Subscriptions: {subscriptions}")
    if len(subscriptions) > 0:
        subscriptions = [
            subscription
            for subscription in subscriptions
            if subscription["attrs"]["status"] == "active"
        ]
    else:
        logger.info(f"No active subscriptions found")

    # Get List of all customers
    customers = (
        supabase_db.table("customers")
        .select("*")
        .order("created", desc=True)
        .execute()
        .data
    )
    unique_customers = {}
    for customer in customers:
        if customer["email"] not in unique_customers:
            unique_customers[customer["email"]] = customer
    customers = list(unique_customers.values())

    # Matching Products
    matching_product_settings = (
        supabase_db.table("product_to_features").select("*").execute()
    ).data

    # if customer.id in subscriptions.customer then find the user id in the table users where email = customer.email and then update the user_settings with is_premium = True else delete the user_settings

    for customer in customers:
        logger.debug(f"Customer: {customer['email']}")
        # Find the subscription of the customer
        user_id = None
        matching_subscription = [
            subscription
            for subscription in subscriptions
            if subscription["customer"] == customer["id"]
        ]
        user_id = (
            supabase_db.table("users")
            .select("id")
            .filter("email", "eq", customer["email"])
            .execute()
        ).data
        if len(user_id) > 0:
            user_id = user_id[0]["id"]
        else:
            logger.debug(f"User not found for customer: {customer['email']}")
            continue
        if len(matching_subscription) > 0:
            logger.debug(
                f"Updating subscription for user {user_id} with subscription {matching_subscription[0]['id']}"
            )
            # Get the matching product from the subscription
            matching_product_settings = [
                product
                for product in matching_product_settings
                if product["stripe_product_id"]
                == matching_subscription[0]["attrs"]["items"]["data"][0]["plan"][
                    "product"
                ]
            ]
            if len(matching_product_settings) > 0:
                # Update the user with the product settings
                supabase_db.table("user_settings").update(
                    {
                        "max_brains": matching_product_settings[0]["max_brains"],
                        "max_brain_size": matching_product_settings[0][
                            "max_brain_size"
                        ],
                        "monthly_chat_credit": matching_product_settings[0][
                            "monthly_chat_credit"
                        ],
                        "api_access": matching_product_settings[0]["api_access"],
                        "models": matching_product_settings[0]["models"],
                        "is_premium": True,
                    }
                ).match({"user_id": str(user_id)}).execute()
            else:
                logger.info(
                    f"No matching product settings found for customer: {customer['email']} with subscription {matching_subscription[0]['id']}"
                )
        else:
            logger.debug(f"No subscription found for customer: {customer['email']}")
            # check if user_settings is_premium is true then delete the user_settings
            user_settings = (
                supabase_db.table("user_settings")
                .select("*")
                .filter("user_id", "eq", user_id)
                .filter("is_premium", "eq", True)
                .execute()
            ).data
            if len(user_settings) > 0:
                supabase_db.table("user_settings").delete().match(
                    {"user_id": user_id}
                ).execute()

    return True


celery.conf.beat_schedule = {
    "remove_onboarding_more_than_x_days_task": {
        "task": f"{__name__}.remove_onboarding_more_than_x_days_task",
        "schedule": crontab(minute="0", hour="0"),
    },
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
