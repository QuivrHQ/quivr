from uuid import UUID

from sqlalchemy import text

from logger import get_logger
from models.settings import get_embeddings, get_pg_database_engine, get_supabase_client
from modules.brain.dto.inputs import BrainUpdatableProperties
from modules.brain.entity.brain_entity import BrainEntity, PublicBrain
from modules.brain.repository.interfaces.brains_interface import BrainsInterface

logger = get_logger(__name__)


class Brains(BrainsInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client
        pg_engine = get_pg_database_engine()
        self.pg_engine = pg_engine

    def create_brain(self, brain):
        embeddings = get_embeddings()
        string_to_embed = f"Name: {brain.name} Description: {brain.description}"
        brain_meaning = embeddings.embed_query(string_to_embed)
        brain_dict = brain.dict(
            exclude={
                "brain_definition",
                "brain_secrets_values",
                "connected_brains_ids",
                "integration",
            }
        )
        brain_dict["meaning"] = brain_meaning
        response = (self.db.table("brains").insert(brain_dict)).execute()

        return BrainEntity(**response.data[0])

    def get_public_brains(self):
        response = (
            self.db.from_("brains")
            .select(
                "id:brain_id, name, description, last_update, brain_type, brain_definition: api_brain_definition(*), number_of_subscribers:brains_users(count)"
            )
            .filter("status", "eq", "public")
            .execute()
        )
        public_brains: list[PublicBrain] = []

        for item in response.data:
            item["number_of_subscribers"] = item["number_of_subscribers"][0]["count"]
            if not item["brain_definition"]:
                del item["brain_definition"]
            else:
                item["brain_definition"]["secrets"] = []

            public_brains.append(PublicBrain(**item))
        return public_brains

    def update_brain_last_update_time(self, brain_id):
        try:
            with self.pg_engine.begin() as connection:
                query = """
                UPDATE brains
                SET last_update = now()
                WHERE brain_id = '{brain_id}'
                """
                connection.execute(text(query.format(brain_id=brain_id)))
        except Exception as e:
            logger.error(e)

    def get_brain_details(self, brain_id):
        with self.pg_engine.begin() as connection:
            query = """
            SELECT * FROM brains
            WHERE brain_id = '{brain_id}'
            """
            response = connection.execute(text(query.format(brain_id=brain_id))).fetchall()
        if len(response) == 0:
            return None
        return BrainEntity(**response[0]._mapping)

    def delete_brain(self, brain_id: str):
        with self.pg_engine.begin() as connection:
            results = connection.execute(
                text(f"DELETE FROM brains WHERE brain_id = '{brain_id}'")
            )

        return results

    def update_brain_by_id(
        self, brain_id: UUID, brain: BrainUpdatableProperties
    ) -> BrainEntity | None:
        embeddings = get_embeddings()
        string_to_embed = f"Name: {brain.name} Description: {brain.description}"
        brain_meaning = embeddings.embed_query(string_to_embed)
        brain_dict = brain.dict(exclude_unset=True)
        brain_dict["meaning"] = brain_meaning
        update_brain_response = (
            self.db.table("brains")
            .update(brain_dict)
            .match({"brain_id": brain_id})
            .execute()
        ).data

        if len(update_brain_response) == 0:
            return None

        return BrainEntity(**update_brain_response[0])

    def get_brain_by_id(self, brain_id: UUID) -> BrainEntity | None:
        # TODO: merge this method with get_brain_details
        with self.pg_engine.begin() as connection:
            response = connection.execute(
                text(f"SELECT * FROM brains WHERE brain_id = '{brain_id}'")
            ).fetchall()

        if len(response) == 0:
            return None
        return BrainEntity(**response[0]._mapping)