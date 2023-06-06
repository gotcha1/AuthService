from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from os import environ
import logging

from models.user_model import User
from config.config import get_settings

logging.getLogger().setLevel(logging.INFO)

config = get_settings()


async def init_db():
    if environ.get("PYTEST_CURRENT_TEST"):
        # Use in-memory MongoDB for pytest
        client = AsyncMongoMockClient()
    else:
        # Create MongoDB motor client
        client = AsyncIOMotorClient(config.DB_URL)

    await init_beanie(client.authdb, document_models=[User])
