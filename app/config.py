
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Phase 2 - Environmental Intelligence Configuration
    API_TITLE: str = "Amoeba Trading System - Phase 2"
    API_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Legacy settings
    app_name: str = "Amoeba Trading Backend"
    api_key: Optional[str] = None
    webhook_secret: Optional[str] = None
    
    # Trading configuration
    default_quantity: float = 1.0
    max_position_size: float = 10000.0
    
    # Database (if needed later)
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
