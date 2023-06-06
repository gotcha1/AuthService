from fastapi import FastAPI
import logging

from api import health_api
from api import user_api
from utils.db import init_db
from config.config import get_settings

logging.getLogger().setLevel(logging.INFO)

config = get_settings()

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.DESCRIPTION,
    version=config.VERSION,
    root_path=config.PATH_PREFIX
)


@app.on_event("startup")
async def app_init():
    await init_db()

    # Add routes
    app.include_router(health_api.router, tags=["health"])
    app.include_router(user_api.router, tags=["user"], prefix='/user')
