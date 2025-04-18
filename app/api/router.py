from fastapi import APIRouter
from app.api.routes.chat import router as chat_router

router = APIRouter()


@router.get("/")
def root():
    return {
        "name": "ai-api-fastapi",
        "description": "AI API with FastAPI",
        "version": "1.0.0",
    }


router.include_router(chat_router)
