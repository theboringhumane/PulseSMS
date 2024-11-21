from typing import Optional

from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    to: str = Field(..., description="Phone number with country code")
    message: str = Field(..., description="Message text to send")


class MessageResponse(BaseModel):
    status: str = Field(..., description="Message status")
    message_id: Optional[str] = Field(None, description="Message ID if sent successfully")
    task_id: Optional[str] = Field(None, description="Task ID if sent successfully")
    message: str = Field(..., description="Response message")
