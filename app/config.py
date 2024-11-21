from enum import Enum
from pydantic_settings import BaseSettings
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
    selenium_host: str = "localhost"
    selenium_port: int = 4444
    debug: bool = False
    headless: bool = True
    urls: dict = {k: v for k, v in URLEnum.__members__.items()}

    class Config:
        env_file = ".env"


settings = Settings()
