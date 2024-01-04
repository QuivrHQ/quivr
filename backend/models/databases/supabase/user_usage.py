from datetime import datetime
from uuid import UUID

from logger import get_logger
from models.databases.repository import Repository

logger = get_logger(__name__)


class UserUsage(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_user_daily_usage(
        self, user_id: UUID, user_email: str, date: datetime, number: int = 1
    ):
        return (
            self.db.table("user_daily_usage")
            .insert(
                {
                    "user_id": str(user_id),
                    "email": user_email,
                    "date": date,
                    "daily_requests_count": number,
                }
            )
            .execute()
        )

    def check_subscription_validity(self, customer_id: str) -> bool:
        """
        Check if the subscription of the user is still valid
        """
        now = datetime.now()

        # Format the datetime object as a string in the appropriate format for your Supabase database
        now_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        subscription_still_valid = (
            self.db.from_("subscriptions")
            .select("*")
            .filter(
                "customer", "eq", customer_id
            )  # then check if current_period_end is greater than now with timestamp format
            .filter("current_period_end", "gt", now_str)
            .execute()
        ).data

        if len(subscription_still_valid) > 0:
            return True

    def check_user_is_customer(self, user_id: UUID) -> (bool, str):
        """
        Check if the user is a customer and return the customer id
        """
        user_email_customer = (
            self.db.from_("users")
            .select("*")
            .filter("id", "eq", str(user_id))
            .execute()
        ).data

        if len(user_email_customer) == 0:
            return False, None

        matching_customers = (
            self.db.table("customers")
            .select("email,id")
            .filter("email", "eq", user_email_customer[0]["email"])
            .execute()
        ).data

        if len(matching_customers) == 0:
            return False, None

        return True, matching_customers[0]["id"]

    def update_customer_settings_with_product_settings(
        self, user_id: UUID, customer_id: str
    ):
        """
        Check if the user is a customer and return the customer id
        """

        matching_products = (
            self.db.table("subscriptions")
            .select("attrs")
            .filter("customer", "eq", customer_id)
            .execute()
        ).data

        # Output object
        # {"id":"sub_1OUZOgJglvQxkJ1H98TSY9bv","plan":{"id":"price_1NwMsXJglvQxkJ1Hbzs5JkTs","active":true,"amount":1900,"object":"plan","created":1696156081,"product":"prod_OjqZPhbBQwmsB8","currency":"usd","interval":"month","livemode":false,"metadata":{},"nickname":null,"tiers_mode":null,"usage_type":"licensed","amount_decimal":"1900","billing_scheme":"per_unit","interval_count":1,"aggregate_usage":null,"transform_usage":null,"trial_period_days":null},"items":{"url":"/v1/subscription_items?subscription=sub_1OUZOgJglvQxkJ1H98TSY9bv","data":[{"id":"si_PJBm1ciQlpaOA4","plan":{"id":"price_1NwMsXJglvQxkJ1Hbzs5JkTs","active":true,"amount":1900,"object":"plan","created":1696156081,"product":"prod_OjqZPhbBQwmsB8","currency":"usd","interval":"month","livemode":false,"metadata":{},"nickname":null,"tiers_mode":null,"usage_type":"licensed","amount_decimal":"1900","billing_scheme":"per_unit","interval_count":1,"aggregate_usage":null,"transform_usage":null,"trial_period_days":null},"price":{"id":"price_1NwMsXJglvQxkJ1Hbzs5JkTs","type":"recurring","active":true,"object":"price","created":1696156081,"product":"prod_OjqZPhbBQwmsB8","currency":"usd","livemode":false,"metadata":{},"nickname":null,"recurring":{"interval":"month","usage_type":"licensed","interval_count":1,"aggregate_usage":null,"trial_period_days":null},"lookup_key":null,"tiers_mode":null,"unit_amount":1900,"tax_behavior":"unspecified","billing_scheme":"per_unit","custom_unit_amount":null,"transform_quantity":null,"unit_amount_decimal":"1900"},"object":"subscription_item","created":1704307355,"metadata":{},"quantity":1,"tax_rates":[],"subscription":"sub_1OUZOgJglvQxkJ1H98TSY9bv","billing_thresholds":null}],"object":"list","has_more":false,"total_count":1},"object":"subscription","status":"active","created":1704307354,"currency":"usd","customer":"cus_PJBmxGOKfQgYDN","discount":null,"ended_at":null,"livemode":false,"metadata":{},"quantity":1,"schedule":null,"cancel_at":null,"trial_end":null,"start_date":1704307354,"test_clock":null,"application":null,"canceled_at":null,"description":null,"trial_start":null,"on_behalf_of":null,"automatic_tax":{"enabled":true},"transfer_data":null,"days_until_due":null,"default_source":null,"latest_invoice":"in_1OUZOgJglvQxkJ1HysujPh0b","pending_update":null,"trial_settings":{"end_behavior":{"missing_payment_method":"create_invoice"}},"pause_collection":null,"payment_settings":{"payment_method_types":null,"payment_method_options":null,"save_default_payment_method":"off"},"collection_method":"charge_automatically","default_tax_rates":[],"billing_thresholds":null,"current_period_end":1706985754,"billing_cycle_anchor":1704307354,"cancel_at_period_end":false,"cancellation_details":{"reason":null,"comment":null,"feedback":null},"current_period_start":1704307354,"pending_setup_intent":null,"default_payment_method":"pm_1OUZOfJglvQxkJ1HSHU0TTWW","application_fee_percent":null,"pending_invoice_item_interval":null,"next_pending_invoice_item_invoice":null}

        # Now extract the product id from the object

        if len(matching_products) == 0:
            logger.info("No matching products found")
            return

        product_id = matching_products[0]["attrs"]["items"]["data"][0]["plan"][
            "product"
        ]

        # Now fetch the product settings

        matching_product_settings = (
            self.db.table("product_to_features")
            .select("*")
            .filter("stripe_product_id", "eq", product_id)
            .execute()
        ).data

        if len(matching_product_settings) == 0:
            logger.info("No matching product settings found")
            return

        product_settings = matching_product_settings[0]

        # Now update the user settings with the product settings
        try:
            self.db.table("user_settings").update(
                {
                    "max_brains": product_settings["max_brains"],
                    "max_brain_size": product_settings["max_brain_size"],
                    "daily_chat_credit": product_settings["daily_chat_credit"],
                    "api_access": product_settings["api_access"],
                    "models": product_settings["models"],
                }
            ).match({"user_id": str(user_id)}).execute()

        except Exception as e:
            logger.error(e)
            logger.error("Error while updating user settings with product settings")

    def check_if_is_premium_user(self, user_id: UUID):
        """
        Check if the user is a premium user
        """
        matching_customers = None
        try:
            user_is_customer, user_customer_id = self.check_user_is_customer(user_id)
            logger.info("🔥🔥🔥")
            logger.info(user_is_customer)
            logger.info(user_customer_id)

            if user_is_customer:
                self.db.table("user_settings").update({"is_premium": True}).match(
                    {"user_id": str(user_id)}
                ).execute()

            if user_is_customer and self.check_subscription_validity(user_customer_id):
                logger.info("User is a premium user")
                self.update_customer_settings_with_product_settings(
                    user_id, user_customer_id
                )
                return True
            else:
                self.db.table("user_settings").update({"is_premium": False}).match(
                    {"user_id": str(user_id)}
                ).execute()
                return False

        except Exception as e:
            logger.info(matching_customers)
            logger.error(e)
            logger.error(
                "Error while checking if user is a premium user. Stripe needs to be configured."
            )
            logger.error(e)
            return False

    def get_user_settings(self, user_id):
        """
        Fetch the user settings from the database
        """

        user_settings_response = (
            self.db.from_("user_settings")
            .select("*")
            .filter("user_id", "eq", str(user_id))
            .execute()
        ).data

        if len(user_settings_response) == 0:
            # Create the user settings
            user_settings_response = (
                self.db.table("user_settings")
                .insert({"user_id": str(user_id)})
                .execute()
            ).data

        if len(user_settings_response) == 0:
            raise ValueError("User settings could not be created")

        user_settings = user_settings_response[0]

        check_is_premium = self.check_if_is_premium_user(user_id)

        if check_is_premium:
            # get the possibly updated user settings
            user_settings_response = (
                self.db.from_("user_settings")
                .select("*")
                .filter("user_id", "eq", str(user_id))
                .execute()
            ).data
            return user_settings_response[0]

        return user_settings

    def get_model_settings(self):
        """
        Fetch the user settings from the database
        """

        model_settings_response = (self.db.from_("models").select("*").execute()).data

        if len(model_settings_response) == 0:
            raise ValueError("An issue occured while fetching the model settings")

        return model_settings_response

    def get_user_usage(self, user_id):
        """
        Fetch the user request stats from the database
        """
        requests_stats = (
            self.db.from_("user_daily_usage")
            .select("*")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return requests_stats.data

    def get_user_requests_count_for_day(self, user_id, date):
        """
        Fetch the user request count from the database
        """
        response = (
            self.db.from_("user_daily_usage")
            .select("daily_requests_count")
            .filter("user_id", "eq", user_id)
            .filter("date", "eq", date)
            .execute()
        ).data

        if response and len(response) > 0:
            return response[0]["daily_requests_count"]
        return 0

    def increment_user_request_count(
        self, user_id, date, current_requests_count: int, number: int = 1
    ):
        """
        Increment the user's requests count for a specific day
        """

        self.update_user_request_count(
            user_id, daily_requests_count=current_requests_count + number, date=date
        )

    def update_user_request_count(self, user_id, daily_requests_count, date):
        response = (
            self.db.table("user_daily_usage")
            .update({"daily_requests_count": daily_requests_count})
            .match({"user_id": user_id, "date": date})
            .execute()
        )

        return response
