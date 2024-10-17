import os
import sqlite3
from uuid import UUID

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Data model for the FetchRequest
class FetchRequest(BaseModel):
    sync_id: int
    user_id: UUID
    notion_api_key: str


# Function to fetch data from Notion if DB doesn't exist
def fetch_notion_data(sync_id: int, user_id: UUID, notion_api_key: str):
    url = "http://notion-fetcher:3002/v1/fetch_store_notion"
    payload = {
        "sync_id": sync_id,
        "user_id": str(user_id),
        "notion_api_key": notion_api_key,
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Notion")
    return response.json()


def get_db_path(sync_id: int):
    db_path = f"/litefs/notion-{sync_id}.db"
    if not os.path.exists(db_path):
        return None
    return db_path


# API route to get all rows from the DB based on sync_id
@app.get("/{sync_id}")
def get_data(sync_id: int, user_id: UUID, notion_api_key: str):
    db_path = get_db_path(sync_id)

    if db_path is None:
        # Database not found, fetch data from Notion
        fetch_notion_data(sync_id, user_id, notion_api_key)
        db_path = get_db_path(sync_id)

        if db_path is None:
            raise HTTPException(status_code=404, detail="Database could not be created")

    # Connect to the SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM notion_pages"
        )  # Replace 'your_table_name' with the actual table name
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"data": rows}
