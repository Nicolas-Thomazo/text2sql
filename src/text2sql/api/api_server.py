from contextlib import asynccontextmanager

from fastapi import FastAPI

from text2sql.api.core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from text2sql.api.core.events import create_start_app_handler
from text2sql.api.routes.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # code to run before app starts
    yield
    # code to run after app stops


def get_application() -> FastAPI:
    application = FastAPI(
        title=PROJECT_NAME, debug=DEBUG, version=VERSION, lifespan=lifespan
    )
    application.include_router(api_router, prefix=API_PREFIX)
    return application


app = get_application()
