from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # local run loads environment variables from load.env; online run loads real environment variables
    PROJECT_NAME: str = os.environ.get("PROJECT_NAME") or "Auth Sevice"
    PATH_PREFIX: str = "/"
    VERSION: str = "1.0.0"
    VOLUME: Path = Path(os.environ.get("VOLUME_MOUNT_PATH", "/data"))
    PORT: str = os.environ.get("PORT") or "8046"
    HOSTNAME_AND_PORT: str = f"{PROJECT_NAME.lower()}:{PORT}"
    DB_NAME: str = os.environ.get("DB_NAME") or "authdb"
    DB_HOST_NAME: str = os.environ.get("DB_HOST_NAME") or "localhost"
    DB_PORT: str = os.environ.get("DB_PORT") or "27017"
    DB_URL = f"mongodb://{DB_HOST_NAME}:{DB_PORT}/{DB_NAME}"

    DESCRIPTION = f"""
        service: {PROJECT_NAME}
        version: {VERSION}
        """


@lru_cache
def get_settings() -> Settings:
    return Settings()
