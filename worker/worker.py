import asyncio

from celery import Celery

from app.config import settings
from app.services.message import MessageService

# Initialize Celery instance
celery_app = Celery('g-messages', broker=settings.celery_broker, backend=settings.celery_result_backend)


# Set default configuration
@celery_app.task(
    bind=True,
    name="app.tasks.send_message",
    queue="messages",
    default_retry_delay=30,
    max_retries=3,
)
def send_message(self, to: str, message: str):
    message_service = MessageService()
    try:
        asyncio.run(message_service.setup())
        # Send message
        asyncio.run(message_service.send_message(to, message))
        message_service.browser.quit()
        return {
            "status": "success",
            "message": "Message sent successfully"
        }
    except Exception as e:
        message_service.browser.quit()
        raise e
