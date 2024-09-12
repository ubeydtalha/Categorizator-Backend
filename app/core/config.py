import logging
import os
from typing import ClassVar

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, ConfigDict, Field
from pydantic_settings import BaseSettings

log_format = logging.Formatter("%(asctime)s : %(levelname)s - %(message)s")

# root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# standard stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
root_logger.addHandler(stream_handler)

logger = logging.getLogger(__name__)

cwd = os.getcwd()
load_dotenv(
    os.path.join(cwd+"/app/", ".env"),
)

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SUPABASE_URL: str = Field(default_factory=lambda: os.getenv("SUPABASE_URL"))
    SUPABASE_KEY: str = Field(default_factory=lambda: os.getenv("SUPABASE_KEY"))
    SUPABASE_DATABASE_URL : str = Field(default_factory=lambda: os.getenv("SUPABASE_DATABASE_URL"))
    # SUPERUSER_EMAIL: str = Field(default_factory=lambda: os.getenv("SUPERUSER_EMAIL"))
    # SUPERUSER_PASSWORD: str = Field(default=lambda: os.getenv("SUPERUSER_PASSWORD"))

    SERVER_HOST: AnyHttpUrl = "https://localhost"
    SERVER_PORT: int = 8000

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    PROJECT_NAME: str = "FastAPI Supabase Item Listing Project"

    # class Config(ConfigDict):
    #     """sensitive to lowercase"""
    #
    #     case_sensitive = True
    Config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)


settings = Settings()