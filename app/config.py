
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Amoeba Trading Backend"
    debug: bool = False
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
