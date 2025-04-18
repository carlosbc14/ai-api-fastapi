from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict


class Message(BaseModel):
    role: Literal["user", "assistant", "system"] = "user"
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    temperature: float = Field(default=0.7, ge=0.1, le=1.5)
    max_tokens: int = Field(default=256, le=256 * 8)


class ChatResponse(BaseModel):
    response: str
    usage: Optional[Dict[str, int]] = None
    finish_reason: Optional[
        Literal["stop", "length", "function_call", "tool_calls"]
    ] = None
