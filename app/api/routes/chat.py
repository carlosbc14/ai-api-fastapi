from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.security import api_key_auth
from app.core.model import generate_response, generate_streaming_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse, dependencies=[Depends(api_key_auth)])
async def chat(request: ChatRequest):
    return await generate_response(request)


@router.post(
    "/stream", response_model=ChatResponse, dependencies=[Depends(api_key_auth)]
)
async def chat_stream(request: Request, body: ChatRequest):
    return EventSourceResponse(generate_streaming_response(request, body))
