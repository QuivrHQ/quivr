use anyhow::bail;
use notion::{
    self,
    models::{paging::PagingCursor, ListResponse, Page},
};
use pyo3::prelude::*;
use reqwest::{
    header::{self, HeaderMap, HeaderValue},
    Client, ClientBuilder,
};
use serde_json::json;
use sqlx::{Sqlite, SqlitePool};

static NOTION_URL: &'static str = "https://api.notion.com/v1/search";
static NOTION_API_VERSION: &'static str = "2022-06-28";

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

            println!(
                "Requesting query: URL: {}, query: {}",
                &NOTION_URL, &query_str
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
                    println!("error parsing request: {:?}", e);
                    break;
                }
            };
        }
        Ok(())
    }
}

async fn save_sqlite<'a>(
    pool: &SqlitePool,
    mut rx: tokio::sync::mpsc::Receiver<Vec<Page>>,
) -> anyhow::Result<()> {
    while let Some(pages) = rx.recv().await {
        println!("Received {} pages ", pages.len());
        bulk_insert_pages(&pool, pages).await.unwrap();
    }
    Ok(())
}

async fn bulk_insert_pages<'a>(pool: &sqlx::Pool<Sqlite>, pages: Vec<Page>) -> anyhow::Result<()> {
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
        match sqlx::query!(
            r#"
            SELECT id
            FROM notion_pages
            WHERE id = $1; "#,
            page_id
        )
        .fetch_one(pool)
        .await
        {
            Ok(_) => {
                // println!("{} page exists. skipping...", page_id)
            }
            Err(sqlx::Error::RowNotFound) => {
                sqlx::query!(
            r#"INSERT INTO notion_pages (id, created_time, last_edited_time, title, archived, parent_id, icon)
            VALUES ($1,$2,$3,$4,$5,$6,$7)
            "#,
            page_id,
            page.created_time,
            page.last_edited_time,
            title,
            page.archived,
            parent_id,
            icon,
        ).execute(pool).await?;
            }
            Err(e) => {
                bail!("error fetching record, {e}")
            }
        }
    }

    Ok(())
}

async fn fetch_save_inner(api_key: String, db_url: String) -> PyResult<()> {
    let pool = SqlitePool::connect(&db_url).await.unwrap();

    let (tx, rx) = tokio::sync::mpsc::channel(1000);
    let client = NotionFetcher::new(api_key, tx)
        .map_err(|_| PyErr::new::<PyAny, _>("can't instanciate client"))?;

    let join = tokio::spawn(async move {
        client.get_all_pages().await.unwrap();
    });

    save_sqlite(&pool, rx)
        .await
        .map_err(|_| PyErr::new::<PyAny, _>("error saving results to sqlite"))?;

    join.await.unwrap();

    PyResult::Ok(())
}

#[pyfunction]
fn fetch_notion_pages(py: Python, api_key: String, db_url: String) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move { fetch_save_inner(api_key, db_url).await })
}

#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fetch_notion_pages, m)?)?;
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
        let db_url = env::var("DATABASE_URL").expect("error loading db_url");
        fetch_save_inner(api_key, db_url).await.unwrap();
    }
}
