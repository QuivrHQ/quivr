use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};
use axum::Json;
use serde::{Deserialize, Serialize};
use serde_json::json;

#[derive(Debug)]
pub enum FetchError {
    RunningFetchError,
    InternalServerError,
}

impl IntoResponse for FetchError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            FetchError::RunningFetchError => {
                (StatusCode::BAD_REQUEST, "Invalid request".to_string())
            }
            FetchError::InternalServerError => (
                StatusCode::INTERNAL_SERVER_ERROR,
                "Internal server error".to_string(),
            ),
        };

        (status, Json(json!({ "error": message }))).into_response()
    }
}

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

#[derive(Serialize, Deserialize, Debug, Eq, PartialEq, Clone)]
pub struct ExtendedPage {
    #[serde(flatten)]
    pub page: notion::models::Page,
    pub url: String,
}
