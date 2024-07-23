from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.models.settings import (
    get_embedding_client,
    get_pg_database_engine,
    get_supabase_client,
)
from quivr_api.modules.brain.dto.inputs import BrainUpdatableProperties
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_api.modules.brain.repository.interfaces.brains_interface import (
    BrainsInterface,
)
from sqlalchemy import text

logger = get_logger(__name__)


class Brains(BrainsInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client
        pg_engine = get_pg_database_engine()
        self.pg_engine = pg_engine

    def create_brain(self, brain):
        embeddings = get_embedding_client()
        string_to_embed = f"Name: {brain.name} Description: {brain.description}"
        brain_meaning = embeddings.embed_query(string_to_embed)
        brain_dict = brain.dict(
            exclude={
                "integration",
            }
        )
        brain_dict["meaning"] = brain_meaning
        response = (self.db.table("brains").insert(brain_dict)).execute()

        return BrainEntity(**response.data[0])

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
            response = connection.execute(
                text(query.format(brain_id=brain_id))
            ).fetchall()
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
        embeddings = get_embedding_client()
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
