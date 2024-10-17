use axum::{
    extract::State,
    http::StatusCode,
    routing::{get, post},
    Json, Router,
};
use notion_fetcher::fetch_and_save;
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    net::SocketAddr,
    sync::{Arc, Mutex},
};
use tokio::{net::TcpListener, task::JoinHandle};
use tower_http::trace::{self, TraceLayer};
use tracing::Level;

use tracing::info;

use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[derive(Clone, Default)]
struct AppState {
    handles: Arc<Mutex<HashMap<usize, JoinHandle<anyhow::Result<()>>>>>,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| {
                format!(
                    "{}=debug,tower_http=debug,axum::rejection=trace",
                    env!("CARGO_CRATE_NAME")
                )
                .into()
            }),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();
    let state = AppState::default();

    let app = Router::new()
        .route("/healthz", get(healthz))
        .route("/v1", post(fetch_notion_pages))
        .with_state(state)
        .layer(
            TraceLayer::new_for_http()
                .make_span_with(trace::DefaultMakeSpan::new().level(Level::INFO))
                .on_response(trace::DefaultOnResponse::new().level(Level::INFO)),
        );

    let listener = TcpListener::bind("0.0.0.0:3002").await.unwrap();

    info!("listening on {}", listener.local_addr().unwrap());
    axum::serve(
        listener,
        app.into_make_service_with_connect_info::<SocketAddr>(),
    )
    .await
    .unwrap();
}

async fn healthz() -> &'static str {
    "Ok"
}

async fn fetch_notion_pages(
    State(state): State<AppState>,
    Json(fetch_request): Json<FetchRequest>,
) -> (StatusCode, Json<FetchResponse>) {
    // TODO:
    let db_url = format!(
        "/litefs/notion-{}-{}.db",
        chrono::offset::Utc::now(),
        &fetch_request.sync_id
    );
    let db = db_url.clone();
    let handle =
        tokio::spawn(async move { fetch_and_save(fetch_request.notion_api_key, db).await });

    let mut handles = state.handles.lock().expect("can't get lock");
    handles.insert(fetch_request.sync_id, handle);
    (
        StatusCode::ACCEPTED,
        FetchResponse { db_path: db_url }.into(),
    )
}

#[derive(Serialize, Deserialize, Debug)]
struct FetchRequest {
    sync_id: usize,
    user_id: uuid::Uuid,
    notion_api_key: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct FetchResponse {
    db_path: String,
}
