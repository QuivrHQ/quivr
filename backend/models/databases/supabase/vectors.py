from models.databases.repository import Repository


class Vector(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def get_vectors_by_file_name(self, file_name):
        response = (
            self.db.table("vectors")
            .select(
                "metadata->>file_name, metadata->>file_size, metadata->>file_extension, metadata->>file_url",
                "content",
                "brains_vectors(brain_id,vector_id)",
            )
            .match({"metadata->>file_name": file_name})
            .execute()
        )

        return response

    def get_vectors_by_file_sha1(self, file_sha1):
        response = (
            self.db.table("vectors")
            .select("id")
            .filter("file_sha1", "eq", file_sha1)
            .execute()
        )

        return response

    def set_file_sha_from_metadata(self, file_sha1):
        # It looks at the file that have a file_sha1 in the metadata that is corresponding but an empty file_sha1 column and set it
        response = (
            self.db.table("vectors")
            .update({"file_sha1": file_sha1})
            .match({"metadata->>file_sha1": file_sha1})
            .execute()
        )

        return response

    def similarity_search(self, query_embedding, table, top_k, threshold):
        response = self.db.rpc(
            table,
            {
                "query_embedding": query_embedding,
                "match_count": top_k,
                "match_threshold": threshold,
            },
        ).execute()
        return response

    def update_summary(self, document_id, summary_id):
        return (
            self.db.table("summaries")
            .update({"document_id": document_id})
            .match({"id": summary_id})
            .execute()
        )

    def get_vectors_by_batch(self, batch_id):
        response = (
            self.db.table("vectors")
            .select(
                "name:metadata->>file_name, size:metadata->>file_size",
                count="exact",
            )
            .eq("id", batch_id)
            .execute()
        )

        return response

    def get_vectors_in_batch(self, batch_ids):
        response = (
            self.db.table("vectors")
            .select(
                "name:metadata->>file_name, size:metadata->>file_size",
                count="exact",
            )
            .in_("id", batch_ids)
            .execute()
        )

        return response
