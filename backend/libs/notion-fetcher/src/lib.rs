use notion::{
    self,
    models::{
        paging::{Paging, PagingCursor},
        search::{DatabaseQuery, NotionSearch, SearchRequest},
        ListResponse, Page,
    },
};
use pyo3::{exceptions::PyValueError, prelude::*};
use reqwest::{
    header::{self, HeaderMap, HeaderValue},
    Client, ClientBuilder,
};
use serde_json::json;

static NOTION_API_VERSION: &'static str = "2022-02-22";

struct NotionFetcher {
    client: Client,
}

impl NotionFetcher {
    fn new(api_token: String) -> anyhow::Result<Self> {
        let mut headers = HeaderMap::new();
        headers.insert(
            "Notion-Version",
            HeaderValue::from_static(NOTION_API_VERSION),
        );
        let mut auth_value = HeaderValue::from_str(&format!("Bearer {}", api_token))?;
        auth_value.set_sensitive(true);
        headers.insert(header::AUTHORIZATION, auth_value);
        let client = ClientBuilder::new().default_headers(headers).build()?;
        Ok(Self { client })
    }

    async fn get_all_pages(&self) -> anyhow::Result<Vec<String>> {
        let url = "https://api.notion.com/v1/search";

        let mut next_cursor: Option<PagingCursor> = None;
        let mut all_pages: Vec<String> = vec![];
        loop {
            let mut query = json!({
                "query":""
            });
            if let Some(cursor) = (&next_cursor).as_ref() {
                query
                    .as_object_mut()
                    .unwrap()
                    .insert("start_cursor".into(), serde_json::to_value(cursor)?);
            }
            let query_str = query.to_string();

            println!("Requesting query: URL: {}, query: {}", &url, &query_str);
            let resp = self
                .client
                .post(url)
                .body(query_str)
                .send()
                .await?
                .json::<ListResponse<notion::models::Object>>()
                .await?;

            resp.results().iter().for_each(|o| match o {
                notion::models::Object::Page { page } => {
                    all_pages.push(page.title().unwrap_or_default())
                }
                _ => {}
            });

            next_cursor = resp.next_cursor;
            if next_cursor.is_none() {
                break;
            } else {
                println!("Fetching more. Current page size {}", all_pages.len());
            }
        }
        println!("{:?}", all_pages);

        Ok(all_pages)
    }
}

async fn fetch_inner(api_key: String) -> PyResult<()> {
    let client = NotionFetcher::new(api_key)
        .map_err(|_| PyErr::new::<PyAny, _>("can't instanciate client"))?;

    client.get_all_pages().await.unwrap();

    // let mut response = client
    //     .search(NotionSearch::Query(String::from("")))
    //     .await
    //     .map_err(|_| PyErr::new::<PyAny, _>("can't fetch the pages"))?;

    // response.results().into_iter().for_each(|o| match o {
    //     notion::models::Object::Page { page } => {
    //         pages.push(page.to_owned());
    //     }
    //     _ => {}
    // });

    PyResult::Ok(())
}

#[pyfunction]
fn fetch_notion_pages(py: Python) -> PyResult<&PyAny> {
    let api_key = "secret_ABCPUWFzI9dFiJqkXcaaZbjYlkcio85mHURvktFC6TC";
    pyo3_asyncio::tokio::future_into_py(py, async move { fetch_inner(api_key.to_string()).await })
}

#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fetch_notion_pages, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test(flavor = "multi_thread", worker_threads = 1)]
    async fn test_fetch() {
        let api_key = "secret_ABCPUWFzI9dFiJqkXcaaZbjYlkcio85mHURvktFC6TC";
        fetch_inner(api_key.to_string()).await.unwrap();
    }
}
