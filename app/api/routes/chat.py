from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.model import generate_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return generate_response(request)
