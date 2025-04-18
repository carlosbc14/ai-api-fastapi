from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.security import api_key_auth
from app.core.model import generate_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(api_key_auth)])
def chat(request: ChatRequest):
    return generate_response(request)
