CREATE TABLE IF NOT EXISTS notion_pages(
    id TEXT PRIMARY KEY,
    created_time DATETIME,
    last_edited_time DATETIME,
    title TEXT,
    archived BOOLEAN,
    public_url TEXT,
    parent_id TEXT,
    cover TEXT,
    icon TEXT,
    properties JSON
);
