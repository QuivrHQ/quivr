from uuid import UUID

from fastapi import APIRouter, Depends, Query

from auth.auth_bearer import (
    AuthBearer,
    get_current_user,  # pyright: ignore reportPrivateUsage=none,
)
from models.brains import Brain
from models.settings import common_dependencies
from models.users import User

explore_router = APIRouter()


@explore_router.get("/explore/", dependencies=[Depends(AuthBearer())], tags=["Explore"])
async def explore_endpoint(  # pyright: ignore reportPrivateUsage=none
    brain_id: UUID = Query(..., description="The ID of the brain"),
    current_user: User = Depends(
        get_current_user,  # pyright: ignore reportPrivateUsage=none
    ),
):
    """
    Retrieve and explore unique user data vectors.
    """
    brain = Brain(id=brain_id)
    unique_data = (  # pyright: ignore reportPrivateUsage=none
        brain.get_unique_brain_files()
    )  # pyright: ignore reportPrivateUsage=none

    unique_data.sort(  # pyright: ignore reportPrivateUsage=none
        key=lambda x: int(x["size"]),  # pyright: ignore reportPrivateUsage=none
        reverse=True,  # pyright: ignore reportPrivateUsage=none
    )
    return {"documents": unique_data}  # pyright: ignore reportPrivateUsage=none


@explore_router.delete(
    "/explore/{file_name}/", dependencies=[Depends(AuthBearer())], tags=["Explore"]
)
async def delete_endpoint(
    file_name: str,
    current_user: User = Depends(
        get_current_user  # pyright: ignore reportPrivateUsage=none
    ),
    brain_id: UUID = Query(..., description="The ID of the brain"),  # noqa: B008
):
    """
    Delete a specific user file by file name.
    """
    brain = Brain(id=brain_id)
    brain.delete_file_from_brain(file_name)

    return {
        "message": f"{file_name} of brain {brain_id} has been deleted by user {current_user.email}."
    }


@explore_router.get(
    "/explore/{file_name}/", dependencies=[Depends(AuthBearer())], tags=["Explore"]
)
async def download_endpoint(  # pyright: ignore reportPrivateUsage=none
    file_name: str,
    current_user: User = Depends(
        get_current_user  # pyright: ignore reportPrivateUsage=none
    ),
):
    """
    Download a specific user file by file name.
    """
    # check if user has the right to get the file: add brain_id to the query

    commons = common_dependencies()
    response = (  # pyright: ignore reportPrivateUsage=none
        commons["supabase"]  # pyright: ignore reportPrivateUsage=none
        .table("vectors")
        .select(
            "metadata->>file_name, metadata->>file_size, metadata->>file_extension, metadata->>file_url",
            "content",
        )
        .match({"metadata->>file_name": file_name})
        .execute()
    )
    documents = response.data  # pyright: ignore reportPrivateUsage=none
    return {"documents": documents}  # pyright: ignore reportPrivateUsage=none
