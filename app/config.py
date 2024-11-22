from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - File: %(filename)s 📁 - Line: %(lineno)d 📍 - Function: %(funcName)s ⚡️ - Message: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class URLEnum(str, Enum):
    AUTH = "https://messages.google.com/web/authentication"
    NEW_MESSAGE = "https://messages.google.com/web/conversations/new"
    CONVERSATIONS = "https://messages.google.com/web/conversations"
    HOME = "https://messages.google.com/web"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore', 
        env_file=".env",
        env_file_encoding="utf-8"
    )
    selenium_host: str
    selenium_port: int
    celery_broker: str
    celery_result_backend: str
    debug: bool = False
    headless: bool = False
    urls: dict = {k: v for k, v in URLEnum.__members__.items()}
    
    
settings = Settings()