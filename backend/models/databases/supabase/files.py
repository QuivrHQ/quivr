from models.databases.repository import Repository


class File(Repository):
    def __init__(self, supabase_client):
        super().__init__(supabase_client)

    def set_file_vectors_ids(self, file_sha1):
        response = (
            self.db.table("vectors")
            .select("id")
            .filter("metadata->>file_sha1", "eq", file_sha1)
            .execute()
        )
        return response.data

    def file_already_exists_in_brain(self, brain_id, file_sha1):
        self.set_file_vectors_ids()
        # Check if file exists in that brain
        response = (
            self.db.table("brains_vectors")
            .select("brain_id, vector_id")
            .filter("brain_id", "eq", brain_id)
            .filter("file_sha1", "eq", file_sha1)
            .execute()
        )
        print("response.data", response.data)
        if len(response.data) == 0:
            return False

        return True
