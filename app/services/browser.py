from typing import Optional, Callable

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from ..config import settings, logger
from ..services.auth import AuthService


class BrowserService:
    def __init__(self, credentials_path: str = "credentials.json"):
        self.driver = None
        self.auth_service = None
        self.credentials_path = credentials_path
        self.setup_driver()

    def setup_driver(self):
        logger.info("File: browser.py 🦊 Line: 20, Function: setup_driver; Setting up Firefox driver")
        firefox_options = Options()

        if settings.headless:
            firefox_options.add_argument("--headless")
        
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Remote(
            command_executor=f"http://{settings.selenium_host}:{settings.selenium_port}/wd/hub",
            options=firefox_options
        )
        self.driver.implicitly_wait(10)

        self.auth_service = AuthService(self.driver, self.credentials_path)
        logger.info("File: browser.py 🦊 Line: 31, Function: setup_driver; Firefox driver setup complete ✅")

    async def authenticate(self, qr_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Start authentication process"""
        if not self.auth_service:
            raise Exception("Browser service not properly initialized")

        return await self.auth_service.start_auth_process(qr_callback)

    def save_credentials(self):
        """Save current session credentials"""
        if self.auth_service:
            self.auth_service.save_credentials()

    def load_credentials(self) -> bool:
        """Load saved credentials"""
        if self.auth_service:
            return self.auth_service.load_credentials()
        return False

    def quit(self):
        if self.driver:
            self.driver.quit()
