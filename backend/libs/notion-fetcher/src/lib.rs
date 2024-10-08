use notion::{self, models::search::NotionSearch};
use pyo3::{exceptions::PyValueError, prelude::*};

#[pyfunction]
fn fetch_notion_pages(py: Python) -> PyResult<&PyAny> {
    let api_key = "secret_ABCPUWFzI9dFiJqkXcaaZbjYlkcio85mHURvktFC6TC";
    let client = notion::NotionApi::new(api_key.to_string())
        .map_err(|_| PyErr::new::<PyValueError, _>("can't init client"))?;
    pyo3_asyncio::tokio::future_into_py(py, async move {
        let pages = client
            .search(NotionSearch::Query(String::from("")))
            .await
            .map_err(|_| PyErr::new::<PyAny, _>("can't fetch the pages"))?;
        println!("{:?}", pages);
        PyResult::Ok(())
    })
}

#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fetch_notion_pages, m)?)?;
    Ok(())
}
