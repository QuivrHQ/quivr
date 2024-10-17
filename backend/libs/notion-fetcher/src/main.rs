use axum::{
    extract::State,
    http::StatusCode,
    routing::{get, post},
    Json, Router,
};
use dotenvy::dotenv;
use notion_fetcher::{fetch_and_save, FetchRequest, FetchResponse};
use std::{
    collections::HashMap,
    env,
    net::SocketAddr,
    sync::{Arc, Mutex},
};
use tokio::{net::TcpListener, task::JoinHandle};
use tower_http::trace::{self, TraceLayer};
use tracing::Level;

use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[derive(Clone, Default)]
struct AppState {
    db_base_path: String,
    handles: Arc<Mutex<HashMap<usize, JoinHandle<anyhow::Result<()>>>>>,
}

#[tokio::main]
async fn main() {
    dotenv().unwrap_or_default();
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| {
                format!("{}=debug,axum::rejection=trace", env!("CARGO_CRATE_NAME")).into()
            }),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Build the state
    let db_base_path = env::var("DB_BASE_PATH").expect("error loading db_url");
    let state = AppState {
        db_base_path,
        ..Default::default()
    };

    // Start router
    let app = Router::new()
        .route("/healthz", get(healthz))
        .route("/v1/fetch_store_notion", post(fetch_notion_pages))
        .with_state(state)
        .layer(
            TraceLayer::new_for_http()
                .make_span_with(trace::DefaultMakeSpan::new().level(Level::INFO))
                .on_response(trace::DefaultOnResponse::new().level(Level::INFO)),
        );

    let listener = TcpListener::bind("0.0.0.0:3002").await.unwrap();

    tracing::info!("listening on {}.", listener.local_addr().unwrap(),);
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
    let FetchRequest { sync_id, .. } = fetch_request;
    let db_url = format!(
        "{}/notion-{}.db",
        state.db_base_path, &fetch_request.sync_id
    );
    let db = db_url.clone();
    let mut handles = state.handles.lock().expect("can't get lock");
    let handle = tokio::spawn(async move { fetch_and_save(fetch_request, db).await });
    handles.insert(sync_id, handle);

    (
        StatusCode::ACCEPTED,
        FetchResponse { db_path: db_url }.into(),
    )
}
