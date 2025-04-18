from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "name": "ai-api-fastapi",
        "description": "AI API with FastAPI",
        "version": "1.0.0",
    }
