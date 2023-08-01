from typing import Optional

from supabase.client import Client


def insert_data_in_table(supabase_client: Client, table_name: str, data: dict):
    response = supabase_client.table(table_name).insert(data).execute()
    return response.data


def update_data_in_table(
    supabase_client: Client,
    table_name: str,
    data: dict,
    identifier: Optional[dict],
):
    response = (
        supabase_client.table(table_name).update(data).match(identifier).execute()
    )
    return response.data


def select_data_in_table(
    supabase_client: Client,
    table_name: str,
    identifier: Optional[dict],
):
    response = supabase_client.table(table_name).select("*").match(identifier).execute()
    return response.data


def delete_data_in_table(
    supabase_client: Client,
    table_name: str,
    identifier: dict,
):
    response = supabase_client.table(table_name).delete().match(identifier).execute()
    return response.data
