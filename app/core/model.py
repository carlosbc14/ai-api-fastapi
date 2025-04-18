from llama_cpp import Llama
from fastapi import HTTPException
from app.core.config import settings
from app.schemas.chat import ChatRequest

try:
    model = Llama(
        model_path=settings.MODEL_PATH,
        chat_format=settings.CHAT_FORMAT,
        n_ctx=settings.CONTEXT_SIZE,
        n_threads=settings.THREADS,
        verbose=settings.VERBOSE,
    )
except Exception as e:
    model = None
    print(f"Error loading model: {e}")


def generate_response(request: ChatRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    response = model.create_chat_completion(
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return {
        "response": response["choices"][0]["message"]["content"].strip(),
        "usage": response.get("usage", {}),
        "finish_reason": response["choices"][0]["finish_reason"],
    }
