from uuid import UUID


def build_secret_unique_name(user_id: UUID, brain_id: UUID, secret_name: str):
    return f"{user_id}-{brain_id}-{secret_name}"
