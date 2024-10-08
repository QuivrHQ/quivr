use anyhow::Result;
use reqwest::Client;
use serde_json::json;

use crate::notion_page::NotionPage;

static BASE_URL: &'static str = "https://api.notion.com/v1/databases/{0}/query";

#[derive(Clone)]
struct NotionClient {
    client: Client,
    access_token: &'static str,
}

impl NotionClient {
    pub fn get_all_pages(&self) -> Result<Vec<NotionPage>> {
        let url = BASE_URL;
        let client = reqwest::blocking::Client::new();

        let mut next_cursor: Option<String> = None;
        let mut all_pages: Vec<NotionPage> = vec![];
        loop {
            let mut query = json!({
                "page_size": 10i32,
                "sorts": [{
                    "timestamp": "created_time",
                    "direction": "ascending",
                }]
            });
            if let Some(cursor) = (&next_cursor).as_ref() {
                query
                    .as_object_mut()
                    .unwrap()
                    .insert("start_cursor".into(), cursor.clone().into());
            }
            let query_str = query.to_string();

            tracing::info!("Requesting query: URL: {}, query: {}", &url, &query_str);
            let resp = client
                .post(url)
                .header("Authorization", "Bearer ".to_string() + &self.api_key)
                .header("Notion-Version", "2022-02-22")
                .header("Content-Type", "application/json")
                .body(query_str)
                .send()?
                .json()?;

            let (mut pages, _next_cursor) = parse_notion_page_list(schema, &resp)?;
            info!("Pages: {:?}", pages.len());
            all_pages.append(&mut pages);
            next_cursor = _next_cursor;

            if next_cursor.is_none() {
                info!("Fetched all items.");
                break;
            } else {
                info!("Has more items.");
            }
        }

        Ok(all_pages)
    }
}
