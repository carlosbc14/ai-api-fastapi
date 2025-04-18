import asyncio
from llama_cpp import Llama
from fastapi import Request, HTTPException
from app.core.config import settings
from app.schemas.chat import ChatRequest
import json

model_lock = asyncio.Lock()

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


async def generate_response(request: ChatRequest):
    try:
        await asyncio.wait_for(model_lock.acquire(), timeout=5)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=429,
            detail="The model is busy. Please try again in a few seconds.",
        )

    try:
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
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error generating response. Please try again in a few seconds.",
        )
    finally:
        model_lock.release()


async def generate_streaming_response(request: Request, body: ChatRequest):
    try:
        await asyncio.wait_for(model_lock.acquire(), timeout=5)
    except asyncio.TimeoutError:
        yield {
            "event": "error",
            "data": json.dumps(
                {"detail": "The model is busy. Please try again in a few seconds."}
            ),
        }
        return

    try:
        if model is None:
            yield {
                "event": "error",
                "data": json.dumps({"detail": "Model not loaded."}),
            }
            return

        full_content = ""
        finish_reason = None

        for response in model.create_chat_completion(
            messages=[{"role": m.role, "content": m.content} for m in body.messages],
            temperature=body.temperature,
            max_tokens=body.max_tokens,
            stream=True,
        ):
            if await request.is_disconnected():
                break

            content = response["choices"][0].get("delta", {}).get("content", "")
            if content:
                full_content += content
                yield {
                    "event": "chunk",
                    "data": json.dumps({"content": content}, ensure_ascii=False),
                }

            finish_reason = response["choices"][0].get("finish_reason")

        yield {"event": "done", "data": json.dumps({"finish_reason": finish_reason})}
    except Exception:
        yield {
            "event": "error",
            "data": json.dumps(
                {
                    "detail": "Error generating response. Please try again in a few seconds."
                }
            ),
        }
    finally:
        model_lock.release()
