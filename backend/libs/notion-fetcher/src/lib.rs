use notion::{
    self,
    models::{paging::PagingCursor, ListResponse, Page},
};
use reqwest::{
    header::{self, HeaderMap, HeaderValue},
    Client, ClientBuilder,
};
use rusqlite::{params, Connection};
use serde::{Deserialize, Serialize};
use serde_json::json;

static NOTION_URL: &'static str = "https://api.notion.com/v1/search";
static NOTION_API_VERSION: &'static str = "2022-06-28";

#[derive(Serialize, Deserialize, Debug)]
pub struct FetchRequest {
    pub sync_id: usize,
    pub user_id: uuid::Uuid,
    pub notion_api_key: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct FetchResponse {
    pub db_path: String,
}

struct NotionFetcher {
    client: Client,
    tx: tokio::sync::mpsc::Sender<Vec<Page>>,
}

impl NotionFetcher {
    fn new(api_token: String, tx: tokio::sync::mpsc::Sender<Vec<Page>>) -> anyhow::Result<Self> {
        let mut headers = HeaderMap::new();
        headers.insert(
            "Notion-Version",
            HeaderValue::from_static(NOTION_API_VERSION),
        );
        headers.insert(
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/json"),
        );
        let mut auth_value = HeaderValue::from_str(&format!("Bearer {}", api_token))?;
        auth_value.set_sensitive(true);
        headers.insert(header::AUTHORIZATION, auth_value);
        let client = ClientBuilder::new().default_headers(headers).build()?;
        Ok(Self { client, tx })
    }

    async fn get_all_pages(&self) -> anyhow::Result<()> {
        let mut next_cursor: Option<PagingCursor> = None;
        loop {
            let mut query = json!({
                "query":"",
                "filter":{"property":"object","value":"page"},
                "sort": {
                    "timestamp": "last_edited_time",
                    "direction": "ascending"
                }
            });
            if let Some(cursor) = (&next_cursor).as_ref() {
                query
                    .as_object_mut()
                    .unwrap()
                    .insert("start_cursor".into(), serde_json::to_value(cursor)?);
            }
            let query_str = query.to_string();

            tracing::debug!(
                "requesting query: URL: {}, query: {}",
                &NOTION_URL,
                &query_str
            );
            match self
                .client
                .post(NOTION_URL)
                .body(query_str)
                .send()
                .await?
                .json::<ListResponse<notion::models::Object>>()
                .await
            {
                Ok(resp) => {
                    let pages: Vec<Page> = resp
                        .results()
                        .into_iter()
                        .filter_map(|o| {
                            if let notion::models::Object::Page { page } = o {
                                Some(page.clone())
                            } else {
                                None
                            }
                        })
                        .collect();
                    if resp.has_more {
                        dbg!(&next_cursor);
                        dbg!(&resp.next_cursor);

                        self.tx.send(pages).await?;

                        let _ = std::mem::replace(&mut next_cursor, resp.next_cursor);
                        if next_cursor.is_none() {
                            break;
                        }
                    }
                }
                Err(e) => {
                    tracing::error!("stopping fetching pages. error parsing request: {:?}", e);
                    break;
                }
            };
        }
        Ok(())
    }
}

fn bulk_insert_pages<'a>(conn: &Connection, pages: Vec<Page>) -> anyhow::Result<()> {
    tracing::debug!("inserting {} pages.", pages.len());

    for page in pages.iter() {
        let parent_id = match &page.parent {
            notion::models::Parent::Page { page_id } => Some(page_id.to_string()),
            _ => None,
        };
        let icon = page
            .icon
            .as_ref()
            .map(|i| match i {
                notion::models::IconObject::Emoji { emoji } => Some(emoji.to_owned()),
                _ => None,
            })
            .flatten();
        let icon = icon.unwrap_or_default();
        let page_id = page.id.to_string();
        let title = page.title().unwrap_or_default();
        conn.execute(
            r#"INSERT OR IGNORE INTO notion_pages (id, created_time, last_edited_time, title, archived, parent_id, icon)
            VALUES (?1,?2,?3,?4,?5,?6,?7)
            "#,
            params![
            page_id,
            page.created_time,
            page.last_edited_time,
            title,
            page.archived,
            parent_id,
            icon,
            ]
        )?;
    }

    Ok(())
}

pub async fn fetch_and_save(fetch_request: FetchRequest, db_url: String) -> anyhow::Result<()> {
    let conn = Connection::open(&db_url)?;
    conn.execute(
        "
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
    );",
        (),
    )?;

    let (tx, mut rx) = tokio::sync::mpsc::channel(1000);
    let client = NotionFetcher::new(fetch_request.notion_api_key, tx)?;

    let join = tokio::spawn(async move {
        client.get_all_pages().await.unwrap();
    });

    while let Some(pages) = rx.recv().await {
        match bulk_insert_pages(&conn, pages) {
            Ok(_) => {}
            Err(e) => {
                tracing::error!("error inserting pages in {}: {:?}", &db_url, e)
            }
        };
    }

    match join.await {
        Ok(_) => {
            tracing::info!("finished fetching pages for {}", &db_url);
        }
        Err(e) => {
            tracing::error!(
                "error fetching pages from notion for user {} sync {}: {:?}",
                fetch_request.user_id,
                fetch_request.sync_id,
                e
            );
        }
    };

    Ok(())
}

#[cfg(test)]
mod tests {
    use std::env;

    use super::*;
    use dotenvy::dotenv;

    #[tokio::test(flavor = "multi_thread", worker_threads = 1)]
    async fn test_fetch() {
        dotenv().expect("can't load dotenv file");
        let api_key = env::var("NOTION_API_KEY").expect("error loading api_key");
        let db_url = String::from("/tmp/notion-1.db");
        let request = FetchRequest {
            sync_id: 1,
            user_id: uuid::Uuid::new_v4(),
            notion_api_key: api_key,
        };
        fetch_and_save(request, db_url).await.unwrap();
    }
}
