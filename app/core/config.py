from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str
    MODEL_PATH: str
    CHAT_FORMAT: str
    CONTEXT_SIZE: int = 4096
    THREADS: int = 2
    VERBOSE: bool = False
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 256

    class Config:
        env_file = ".env"


settings = Settings()
