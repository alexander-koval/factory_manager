from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).parent.parent.parent
DATABASE_FILE = ROOT_DIR / "database.db"


class Settings(BaseSettings):
    database_url: str = f"sqlite+aiosqlite:///{DATABASE_FILE}"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
