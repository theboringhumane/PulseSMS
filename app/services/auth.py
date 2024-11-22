import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config import settings, logger
from ..utils.selectors import XPathSelectors
import json
import os
from typing import Optional, Callable, Any, Coroutine


class AuthService:
    def __init__(self, driver: webdriver, credentials_path: str = "credentials.json"):
        self.driver = driver
        self.credentials_path = credentials_path
        self.is_authenticated = False
        self.qr_callback: Optional[Coroutine[Any, Any, None]] = None

    async def check_existing_auth(self) -> bool:
        try:
            logger.info("Function: check_existing_auth; Checking existing auth")
            self.driver.get(settings.urls["CONVERSATIONS"])

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPathSelectors.CONVERSATION_LIST))
            )

            self.is_authenticated = True
            logger.info("Function: check_existing_auth; Restored session! ✅")
            return True

        except Exception as e:
            logger.info("Function: check_existing_auth; No existing session found! ❌")
            return False

    async def check_remember_me(self):
        try:
            logger.info("Function: check_remember_me; Checking remember me slider")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPathSelectors.REMEMBER_ME_SLIDER))
            )

            slider_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPathSelectors.REMEMBER_ME_SLIDER_BUTTON))
            )

            class_name = slider_btn.get_attribute("class")
            is_checked = "checked" in class_name

            if not is_checked:
                slider_btn.click()
                logger.info("Function: check_remember_me; Checked remember me! ✅")

        except Exception as e:
            logger.error(f"Function: check_remember_me; Error checking remember me: {str(e)} ❌")
            raise Exception("Could not find remember me slider")

    async def attach_qr_code_listener(self):
        try:
            logger.info("File: auth.py 🎧 Line: 82, Function: attach_qr_code_listener; Attaching QR code listener")
            # Wait for QR code element
            qr_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPathSelectors.QR_CODE))
            )

            # Execute JavaScript to observe QR code changes
            script = """
            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    mutation.addedNodes.forEach((node) => {
                        if (node instanceof HTMLImageElement) {
                            node.onload = () => {
                                window.latestQRImage = node.src;  // Store the new image source
                            }
                        }
                    });
                }
            });

            observer.observe(arguments[0], {
                attributes: true,
                childList: true,
                characterData: true,
                subtree: true
            });
            """

            # Create a wrapper function that sets the latestQRImage
            wrapper_script = """
            window.latestQRImage = null;  // Initialize the variable
            """
            self.driver.execute_script(wrapper_script)

            # Start observing
            self.driver.execute_script(script, qr_element)

            # Polling to check for changes in window.latestQRImage
            previous_image = None
            while True:
                # Get the current image from the window variable
                current_image = self.driver.execute_script("return window.latestQRImage;")

                if current_image and current_image != previous_image:
                    if self.qr_callback:
                        return await self.qr_callback(current_image)
                    else:
                        logger.info("File: auth.py 🎧 Line: 124, Function: attach_qr_code_listener; QR code callback not set")
                        return current_image
                # Sleep for a short interval before checking again
                await asyncio.sleep(0.2)  # Use asyncio.sleep for async sleep

        except Exception as e:
            logger.error(
                f"File: auth.py ❌ Line: 137, Function: attach_qr_code_listener; Error attaching QR listener: {str(e)}")
            raise Exception("Could not attach QR code listener")

    async def start_auth_process(self, qr_callback: Optional[Callable[[str], None]] = None):
        """Start the authentication process"""
        self.qr_callback = qr_callback

        # Check existing auth first
        if await self.check_existing_auth():
            return True

        # If no existing auth, start new auth process
        try:
            logger.info("Function: start_auth_process; Starting new auth process")
            self.driver.get(settings.urls["AUTH"])

            await self.check_remember_me()

            async def post_qr_code_callback() -> bool:
                logger.info("Function: start_auth_process; Waiting for authentication...")
                # Wait for authentication
                WebDriverWait(self.driver, 200).until(  # 3 minutes timeout
                    lambda driver: "/conversations" in driver.current_url
                )

                self.is_authenticated = True
                logger.info("Function: start_auth_process; Authentication successful! ✅")
                return True

            await self.attach_qr_code_listener()
            return await post_qr_code_callback()
        except Exception as e:
            logger.error(f"Function: start_auth_process; Authentication failed: {str(e)} ❌")
            return False

    def save_credentials(self):
        """Save session credentials to file"""
        if not self.is_authenticated:
            return

        try:
            cookies = self.driver.get_cookies()
            local_storage = self.driver.execute_script("return window.localStorage;")

            credentials = {
                "cookies": cookies,
                "localStorage": local_storage
            }

            with open(self.credentials_path, 'w') as f:
                json.dump(credentials, f)

            logger.info("Function: save_credentials; Credentials saved successfully ✅")

        except Exception as e:
            logger.error(f"Function: save_credentials; Error saving credentials: {str(e)} ❌")

    def load_credentials(self) -> bool:
        """Load credentials from file"""
        try:
            if not os.path.exists(self.credentials_path):
                return False

            with open(self.credentials_path, 'r') as f:
                credentials = json.load(f)

            self.driver.get(
                settings.urls["HOME"]
            )

            # Set cookies
            for cookie in credentials.get("cookies", []):
                self.driver.add_cookie(cookie)

            # Set localStorage
            for key, value in credentials.get("localStorage", {}).items():
                self.driver.execute_script(
                    f"window.localStorage.setItem('{key}', '{value}')"
                )

            logger.info("Function: load_credentials; Credentials loaded successfully ✅")
            return True

        except Exception as e:
            logger.error(f"Function: load_credentials; Error loading credentials: {str(e)} ❌")
            return False
