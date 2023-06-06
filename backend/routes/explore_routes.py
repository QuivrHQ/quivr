from auth.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends
from models.users import User
from utils.vectors import CommonsDep

explore_router = APIRouter()

@explore_router.get("/explore", dependencies=[Depends(JWTBearer())])
async def explore_endpoint(commons: CommonsDep,credentials: dict = Depends(JWTBearer()) ):
    user = User(email=credentials.get('email', 'none'))
    response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact").filter("user_id", "eq", user.email).execute()
    documents = response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    unique_data = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    # Sort the list of documents by size in decreasing order
    unique_data.sort(key=lambda x: int(x['size']), reverse=True)

    return {"documents": unique_data}


@explore_router.delete("/explore/{file_name}", dependencies=[Depends(JWTBearer())])
async def delete_endpoint(commons: CommonsDep, file_name: str, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    # Cascade delete the summary from the database first, because it has a foreign key constraint
    commons['supabase'].table("summaries").delete().match(
        {"metadata->>file_name": file_name}).execute()
    commons['supabase'].table("vectors").delete().match(
        {"metadata->>file_name": file_name, "user_id": user.email}).execute()
    return {"message": f"{file_name} of user {user.email} has been deleted."}


@explore_router.get("/explore/{file_name}", dependencies=[Depends(JWTBearer())])
async def download_endpoint(commons: CommonsDep, file_name: str,credentials: dict = Depends(JWTBearer()) ):
    user = User(email=credentials.get('email', 'none'))
    response = commons['supabase'].table("vectors").select(
        "metadata->>file_name, metadata->>file_size, metadata->>file_extension, metadata->>file_url", "content").match({"metadata->>file_name": file_name, "user_id": user.email}).execute()
    documents = response.data
    # Returns all documents with the same file name
    return {"documents": documents}
