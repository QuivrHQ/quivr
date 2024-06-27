import json
import os

import msal
import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()

CLIENT_ID = "511dce23-02f3-4724-8684-05da226df5f3"
AUTHORITY = "https://login.microsoftonline.com/common"
REDIRECT_URI = "http://localhost:8000/oauth2callback"
SCOPE = [
    "https://graph.microsoft.com/Files.Read",
    "https://graph.microsoft.com/User.Read",
    "https://graph.microsoft.com/Sites.Read.All",
]

client = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)


def get_token_data():
    if not os.path.exists("azure_token.json"):
        raise HTTPException(status_code=401, detail="User not authenticated")
    with open("azure_token.json", "r") as token_file:
        token_data = json.load(token_file)
    if "access_token" not in token_data:
        raise HTTPException(status_code=401, detail="Invalid token data")
    return token_data


def refresh_token():
    if not os.path.exists("azure_token.json"):
        raise HTTPException(status_code=401, detail="User not authenticated")
    with open("azure_token.json", "r") as token_file:
        token_data = json.load(token_file)
    if "refresh_token" not in token_data:
        raise HTTPException(status_code=401, detail="No refresh token available")

    result = client.acquire_token_by_refresh_token(
        token_data["refresh_token"], scopes=SCOPE
    )
    if "access_token" not in result:
        raise HTTPException(status_code=400, detail="Failed to refresh token")

    with open("azure_token.json", "w") as token:
        json.dump(result, token)

    return result


def get_headers(token_data):
    return {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Accept": "application/json",
    }


@app.get("/authorize")
def authorize():
    authorization_url = client.get_authorization_request_url(
        scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    return JSONResponse(content={"authorization_url": authorization_url})


@app.get("/oauth2callback")
def oauth2callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    result = client.acquire_token_by_authorization_code(
        code, scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    if "access_token" not in result:
        print(f"Token acquisition failed: {result}")
        raise HTTPException(status_code=400, detail="Failed to acquire token")

    with open("azure_token.json", "w") as token:
        json.dump(result, token)

    return JSONResponse(content={"message": "Authentication successful"})


@app.get("/list_sites")
def list_sites(token_data: dict = Depends(get_token_data)):
    headers = get_headers(token_data)
    endpoint = "https://graph.microsoft.com/v1.0/sites?search=*"
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 401:
        token_data = refresh_token()
        headers = get_headers(token_data)
        response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    sites = response.json().get("value", [])
    return JSONResponse(content={"sites": sites})


def extract_files_and_folders(items, headers, page_size):
    result = []
    for item in items:
        entry = {
            "name": item.get("name"),
            "id": item.get("id"),
            "parentReference": item.get("parentReference"),
            "lastModifiedDateTime": item.get("lastModifiedDateTime"),
            "webUrl": item.get("webUrl"),
            "size": item.get("size"),
            "fileSystemInfo": item.get("fileSystemInfo"),
            "folder": item.get("folder"),
            "file": item.get("file"),
        }
        if "folder" in item:
            folder_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{item['id']}/children?$top={page_size}"
            children = []
            while folder_endpoint:
                folder_response = requests.get(folder_endpoint, headers=headers)
                if folder_response.status_code == 200:
                    children_page = folder_response.json().get("value", [])
                    children.extend(children_page)
                    folder_endpoint = folder_response.json().get(
                        "@odata.nextLink", None
                    )
                else:
                    break
            entry["children"] = extract_files_and_folders(children, headers, page_size)
        result.append(entry)
    return result


def fetch_all_files(headers, page_size):
    endpoint = (
        f"https://graph.microsoft.com/v1.0/me/drive/root/children?$top={page_size}"
    )
    all_files = []
    while endpoint:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 401:
            token_data = refresh_token()
            headers = get_headers(token_data)
            response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        files = response.json().get("value", [])
        all_files.extend(files)
        endpoint = response.json().get("@odata.nextLink", None)
    return all_files


@app.get("/list_files")
def list_files(page_size: int = 1, token_data: dict = Depends(get_token_data)):
    headers = get_headers(token_data)
    all_files = fetch_all_files(headers, page_size)
    structured_files = extract_files_and_folders(all_files, headers, page_size)
    return JSONResponse(content={"files": structured_files})


@app.get("/download_file/{file_id}")
def download_file(file_id: str, token_data: dict = Depends(get_token_data)):
    headers = get_headers(token_data)
    metadata_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
    metadata_response = requests.get(metadata_endpoint, headers=headers)
    if metadata_response.status_code == 401:
        token_data = refresh_token()
        headers = get_headers(token_data)
        metadata_response = requests.get(metadata_endpoint, headers=headers)
    if metadata_response.status_code != 200:
        raise HTTPException(
            status_code=metadata_response.status_code, detail=metadata_response.text
        )
    metadata = metadata_response.json()
    if "folder" in metadata:
        raise HTTPException(
            status_code=400, detail="The specified ID is a folder, not a file"
        )
    download_endpoint = (
        f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
    )
    download_response = requests.get(download_endpoint, headers=headers, stream=True)
    if download_response.status_code == 401:
        token_data = refresh_token()
        headers = get_headers(token_data)
        download_response = requests.get(
            download_endpoint, headers=headers, stream=True
        )
    if download_response.status_code != 200:
        raise HTTPException(
            status_code=download_response.status_code, detail=download_response.text
        )
    return StreamingResponse(
        download_response.iter_content(chunk_size=1024),
        headers={"Content-Disposition": f"attachment; filename={metadata.get('name')}"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
