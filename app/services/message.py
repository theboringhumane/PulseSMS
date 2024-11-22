import asyncio

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..config import settings, logger
from ..services.browser import BrowserService
from ..utils.selectors import XPathSelectors


class MessageService:
    def __init__(self):
        self.browser = BrowserService()
        self.driver = self.browser.driver

    async def setup(self):
        if self.browser.load_credentials():
            await self.browser.authenticate()

    async def open_message_page(self):
        print("Opening message page")
        print(self.driver)

        self.driver.get(settings.urls["NEW_MESSAGE"])

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, XPathSelectors.CONTACT_INPUT))
        )

    async def send_message(self, to: str, message: str) -> dict:
        logger.info(f"Function: send_message; Sending message to={to}")
        try:
            await self.open_message_page()
            # Type contact
            contact_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPathSelectors.CONTACT_INPUT))
            )
            contact_input.send_keys(to)

            # Wait for loader to disappear and click contact selector
            loader = WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "loader"))
            )
            logger.info("File: message.py 📱 Line: 45, Function: send_message; Loader disappeared")

            selector_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, XPathSelectors.CONTACT_SELECTOR_BTN))
            )
            selector_btn.click()

            # Type message
            textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPathSelectors.TYPE_TEXTAREA))
            )
            textarea.send_keys(message)

            # // press enter to send message\
            textarea.send_keys(u'\ue007') \
 \
                # wait for message to be sent
            await asyncio.sleep(0.1)
            # get all mws-message-wrapper elements and last one is the message sent
            status_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, XPathSelectors.STATUS_MESSAGE))
            )[-1]

            return {
                "status": "success",
                "message_id": status_element.get_attribute("msg-id") if status_element else None
            }

        except Exception as e:
            logger.error(f"Function: send_message; Error={str(e)}")
            raise Exception(f"Failed to send message: {str(e)}")
