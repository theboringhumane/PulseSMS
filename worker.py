import asyncio

from celery.app import Celery
from celery.signals import worker_shutdown, worker_process_init, worker_ready

from app.services.message import MessageService

# Initialize Celery instance
celery_app = Celery('g-messages', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Load tasks from tasks module
celery_app.autodiscover_tasks(['app.tasks'])

# Initialize message service set a global variable but not initialized
message_service = MessageService()


# Set default configuration
@celery_app.task(
    bind=True,
    name="app.tasks.send_message",
    queue="messages",
    default_retry_delay=30,
    max_retries=3,
)
def send_message(self, to: str, message: str):
    # Send message
    asyncio.run(message_service.send_message(to, message))
    return True


@worker_ready.connect
def setup(sender, signal, **kwargs):
    asyncio.run(message_service.setup())


@worker_shutdown.connect
def cleanup(sender, signal, **kwargs):
    message_service.browser.quit()
    print("Browser closed")
    print("Worker cleanup complete")
    exit(0)
