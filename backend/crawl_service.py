from packages.utils import handle_request_validation_error

if __name__ == "__main__":
    # import needed here when running main.py to debug backend
    # you will need to run pip install python-dotenv
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from logger import get_logger
from middlewares.cors import add_cors_middleware
from modules.misc.controller import misc_router
from routes.crawl_routes import crawl_router

logger = get_logger(__name__)
app = FastAPI()

add_cors_middleware(app)


app.include_router(crawl_router)
app.include_router(misc_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


handle_request_validation_error(app)

if __name__ == "__main__":
    # run main.py to debug backend
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5050)
