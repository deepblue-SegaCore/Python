from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    API_TITLE: str = "Amoeba Trading System"
    API_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Webhook Settings
    WEBHOOK_SECRET: Optional[str] = None

    # Trading Configuration
    DEFAULT_QUANTITY: float = 1.0
    MAX_POSITION_SIZE: float = 10000.0

    class Config:
        env_file = ".env"

settings = Settings()