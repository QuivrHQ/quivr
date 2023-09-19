from models.databases.repository import Repository


class File(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def set_file_vectors_ids(self, file_sha1):
        response = (
            self.db.table("vectors")
            .select("id")
            .filter("file_sha1", "eq", file_sha1)
            .execute()
        )
        return response.data

    def get_brain_vectors_by_brain_id_and_file_sha1(self, brain_id, file_sha1):
        self.set_file_vectors_ids(file_sha1)
        # Check if file exists in that brain
        response = (
            self.db.table("brains_vectors")
            .select("brain_id, vector_id")
            .filter("brain_id", "eq", str(brain_id))
            .filter("file_sha1", "eq", file_sha1)
            .execute()
        )

        return response
