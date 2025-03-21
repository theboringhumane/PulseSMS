import base64
import uuid

from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.staticfiles import StaticFiles

from app.config import logger
from app.schemas.message import MessageRequest, MessageResponse
from app.services.message import MessageService
from worker.worker import celery_app

app = FastAPI(title="Google Messages API")

app.mount("/auth", StaticFiles(html=True, directory="static"), name="auth")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.websocket("/ws/auth")
async def websocket_auth_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({
        "type": "info",
        "data": "We're setting up the browser, please wait... This is a one-time setup"
    })

    # Initialize message service set a global variable but not initialized
    message_service = MessageService()

    await message_service.setup()

    async def qr_callback(base64_image: str):
        logger.info(
            f"File: main.py 📸 Line: 47, Function: qr_callback; Sending QR code to client {len(base64_image)} bytes"
        )
        logger.info(
            base64_image
        )
        with open("static/qr_code.png", "wb") as f:
            f.write(
                base64.b64decode(
                    base64_image.split(",")[1]
                )
            )
        await websocket.send_json({
            "type": "qr-code",
            "data": base64_image
        })
        return True

    try:
        await websocket.send_json({
            "type": "info",
            "data": "Please scan the QR code to authenticate, this will only happen once"
        })
        # Start authentication process
        auth_result = await message_service.browser.authenticate(qr_callback)

        if auth_result:
            # Save credentials on successful auth
            message_service.browser.save_credentials()
            await websocket.send_json({
                "type": "authenticated",
                "data": "Authentication successful!"
            })
        else:
            print("Authentication failed!")
            await websocket.send_json({
                "type": "error",
                "data": "Authentication failed!"
            })

    except Exception as e:

        print(f"Error: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "data": str(e)
        })
        # Close the WebSocket connection
    finally:
        if message_service.browser:
            message_service.browser.quit()
        await websocket.close()


@app.get("/api/messages/task/{task_id}")
async def get_task_result(task_id: str):
    # Retrieve task result
    result = AsyncResult(task_id, app=celery_app)
    if result.ready():
        return {"result": result.get()}
    else:
        return {"status": "pending"}


@app.post("/api/messages/send", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    try:
        # Add message to background task queue
        logger.info(f"File: main.py 📨 Line: 55, Function: send_message; Adding message to queue to={request.to}")
        # Create background task to send message and return task id
        task = celery_app.send_task(
            "app.tasks.send_message",
            args=(request.to, request.message)
        )

        # Return immediate response
        return MessageResponse(
            status="queued",
            message_id=str(uuid.uuid4()),
            task_id=task.id,
            message="Message added to queue and will be sent shortly"
        )
    except Exception as e:
        logger.error(f"Function: send_message; Error={str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
