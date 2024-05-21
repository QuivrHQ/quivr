import json
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = FastAPI()

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
CLIENT_SECRETS_FILE = "credentials.json"
REDIRECT_URI = "http://localhost:8000/oauth2callback"

# Disable OAuthlib's HTTPS verification when running locally.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@app.get("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    # Store the state in session to validate the callback later
    with open("state.json", "w") as state_file:
        json.dump({"state": state}, state_file)
    return JSONResponse(content={"authorization_url": authorization_url})


@app.get("/oauth2callback")
def oauth2callback(request: Request):
    state = request.query_params.get("state")
    with open("state.json", "r") as state_file:
        saved_state = json.load(state_file)["state"]

    if state != saved_state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state, redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=str(request.url))
    creds = flow.credentials

    # Save the credentials for future use
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return JSONResponse(content={"message": "Authentication successful"})


@app.get("/list_files")
def list_files():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            raise HTTPException(status_code=401, detail="Credentials are not valid")

    try:
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            return JSONResponse(content={"files": "No files found."})

        files = [{"name": item["name"], "id": item["id"]} for item in items]
        return JSONResponse(content={"files": files})
    except HttpError as error:
        raise HTTPException(status_code=500, detail=f"An error occurred: {error}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
