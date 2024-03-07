from logger import get_logger
from models.settings import get_supabase_client
from modules.brain.repository.interfaces.brains_vectors_interface import (
    BrainsVectorsInterface,
)

logger = get_logger(__name__)


class BrainsVectors(BrainsVectorsInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def create_brain_vector(self, brain_id, vector_id, file_sha1):
        response = (
            self.db.table("brains_vectors")
            .insert(
                {
                    "brain_id": str(brain_id),
                    "vector_id": str(vector_id),
                    "file_sha1": file_sha1,
                }
            )
            .execute()
        )
        return response.data

    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        # move to vectors class
        vectorsResponse = (
            self.db.table("vectors")
            .select("id")
            .filter("file_sha1", "eq", file_sha1)
            .execute()
        )
        return vectorsResponse.data

    def get_brain_vector_ids(self, brain_id):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        response = (
            self.db.from_("brains_vectors")
            .select("vector_id")
            .filter("brain_id", "eq", brain_id)
            .execute()
        )

        vector_ids = [item["vector_id"] for item in response.data]

        if len(vector_ids) == 0:
            return []

        return vector_ids

    def delete_file_from_brain(self, brain_id, file_name: str):
        # First, get the vector_ids associated with the file_name
        # TODO: filter by brain_id
        file_vectors = (
            self.db.table("vectors")
            .select("id")
            .filter("metadata->>file_name", "eq", file_name)
            .execute()
        )

        file_vectors_ids = [item["id"] for item in file_vectors.data]

        # remove current file vectors from brain vectors
        self.db.table("brains_vectors").delete().filter(
            "vector_id", "in", f"({','.join(map(str, file_vectors_ids))})"
        ).filter("brain_id", "eq", brain_id).execute()

        vectors_used_by_another_brain = (
            self.db.table("brains_vectors")
            .select("vector_id")
            .filter("vector_id", "in", f"({','.join(map(str, file_vectors_ids))})")
            .filter("brain_id", "neq", brain_id)
            .execute()
        )

        vectors_used_by_another_brain_ids = [
            item["vector_id"] for item in vectors_used_by_another_brain.data
        ]

        vectors_no_longer_used_ids = [
            id for id in file_vectors_ids if id not in vectors_used_by_another_brain_ids
        ]

        self.db.table("vectors").delete().filter(
            "id", "in", f"({','.join(map(str, vectors_no_longer_used_ids))})"
        ).execute()

        return {"message": f"File {file_name} in brain {brain_id} has been deleted."}

    def delete_brain_vector(self, brain_id: str):
        results = (
            self.db.table("brains_vectors")
            .delete()
            .match({"brain_id": brain_id})
            .execute()
        )

        return results
