from uuid import UUID

from posthog import Posthog
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrainRateLimiting(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)
    max_brain_per_user: int = 5


class SendEmailSettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)
    resend_contact_sales_from: str = "null"
    resend_contact_sales_to: str = "null"


# The `PostHogSettings` class is used to initialize and interact with the PostHog analytics service.
class PostHogSettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)
    posthog_api_key: str | None = None
    posthog_api_url: str | None = None
    posthog: Posthog | None = None

    def __init__(self, *args, **kwargs):
        """
        The function initializes the "posthog" attribute and calls the "initialize_posthog" method.
        """
        super().__init__(*args, **kwargs)
        self.posthog = None
        self.initialize_posthog()

    def initialize_posthog(self):
        """
        The function initializes a PostHog client with an API key and URL.
        """
        if self.posthog_api_key and self.posthog_api_url:
            self.posthog = Posthog(
                api_key=self.posthog_api_key, host=self.posthog_api_url
            )

    def log_event(self, user_id: UUID, event_name: str, event_properties: dict):
        """
        The function logs an event with a user ID, event name, and event properties using the PostHog
        analytics tool.

        :param user_id: The user_id parameter is a UUID (Universally Unique Identifier) that uniquely
        identifies a user. It is typically used to track and identify individual users in an application
        or system
        :type user_id: UUID
        :param event_name: The event_name parameter is a string that represents the name or type of the
        event that you want to log. It could be something like "user_signed_up", "item_purchased", or
        "page_viewed"
        :type event_name: str
        :param event_properties: The event_properties parameter is a dictionary that contains additional
        information or properties related to the event being logged. These properties provide more
        context or details about the event and can be used for analysis or filtering purposes
        :type event_properties: dict
        """
        if self.posthog:
            self.posthog.capture(user_id, event_name, event_properties)

    def set_user_properties(self, user_id: UUID, event_name, properties: dict):
        """
        The function sets user properties for a given user ID and event name using the PostHog analytics
        tool.

        :param user_id: The user_id parameter is a UUID (Universally Unique Identifier) that uniquely
        identifies a user. It is used to associate the user with the event and properties being captured
        :type user_id: UUID
        :param event_name: The `event_name` parameter is a string that represents the name of the event
        that you want to capture. It could be something like "user_signed_up" or "item_purchased"
        :param properties: The `properties` parameter is a dictionary that contains the user properties
        that you want to set. Each key-value pair in the dictionary represents a user property, where
        the key is the name of the property and the value is the value you want to set for that property
        :type properties: dict
        """
        if self.posthog:
            self.posthog.capture(
                user_id, event=event_name, properties={"$set": properties}
            )

    def set_once_user_properties(self, user_id: UUID, event_name, properties: dict):
        """
        The function sets user properties for a specific event, ensuring that the properties are only
        set once.

        :param user_id: The user_id parameter is a UUID (Universally Unique Identifier) that uniquely
        identifies a user
        :type user_id: UUID
        :param event_name: The `event_name` parameter is a string that represents the name of the event
        that you want to capture. It could be something like "user_signed_up" or "item_purchased"
        :param properties: The `properties` parameter is a dictionary that contains the user properties
        that you want to set. Each key-value pair in the dictionary represents a user property, where
        the key is the property name and the value is the property value
        :type properties: dict
        """
        if self.posthog:
            self.posthog.capture(
                user_id, event=event_name, properties={"$set_once": properties}
            )


class BrainSettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)
    openai_api_key: str = ""
    azure_openai_embeddings_url: str = ""
    supabase_url: str = ""
    supabase_service_key: str = ""
    resend_api_key: str = "null"
    resend_email_address: str = "brain@mail.quivr.app"
    ollama_api_base_url: str | None = None
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    pg_database_url: str
    pg_database_async_url: str
    embedding_dim: int = 1536


class ResendSettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)
    resend_api_key: str = "null"
    quivr_smtp_server: str = ""
    quivr_smtp_port: int = 587
    quivr_smtp_username: str = ""
    quivr_smtp_password: str = ""


class ParseableSettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)
    use_parseable: bool = False
    parseable_url: str | None = None
    parseable_auth: str | None = None
    parseable_stream_name: str | None = None


settings = BrainSettings()  # type: ignore
parseable_settings = ParseableSettings()
