from uuid import UUID

from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from logger import get_logger
from models.databases.supabase.supabase import SupabaseDB
from posthog import Posthog
from pydantic import BaseSettings
from supabase.client import Client, create_client
from vectorstore.supabase import SupabaseVectorStore

logger = get_logger(__name__)


class BrainRateLimiting(BaseSettings):
    max_brain_per_user: int = 5


# The `PostHogSettings` class is used to initialize and interact with the PostHog analytics service.
class PostHogSettings(BaseSettings):
    posthog_api_key: str = None
    posthog_api_url: str = None
    posthog: Posthog = None

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
    openai_api_key: str
    supabase_url: str
    supabase_service_key: str
    resend_api_key: str = "null"
    resend_email_address: str = "brain@mail.quivr.app"
    ollama_api_base_url: str = None


class ResendSettings(BaseSettings):
    resend_api_key: str = "null"


def get_supabase_client() -> Client:
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    supabase_client: Client = create_client(
        settings.supabase_url, settings.supabase_service_key
    )
    return supabase_client


def get_supabase_db() -> SupabaseDB:
    supabase_client = get_supabase_client()
    return SupabaseDB(supabase_client)


def get_embeddings():
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    if settings.ollama_api_base_url:
        embeddings = OllamaEmbeddings(
            base_url=settings.ollama_api_base_url,
        )  # pyright: ignore reportPrivateUsage=none
    else:
        embeddings = OpenAIEmbeddings()  # pyright: ignore reportPrivateUsage=none
    return embeddings


def get_documents_vector_store() -> SupabaseVectorStore:
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    embeddings = get_embeddings()
    supabase_client: Client = create_client(
        settings.supabase_url, settings.supabase_service_key
    )
    documents_vector_store = SupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors"
    )
    return documents_vector_store
