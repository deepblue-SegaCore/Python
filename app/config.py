
"""
Configuration settings for Amoeba Trading System
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    API_VERSION = "2.0.0"
    API_TITLE = "Amoeba Trading System"
    
    # Biological Constants (from research)
    MEMORY_DURATION_MINUTES = 95  # Amoeba memory limit
    LEARNING_SUCCESS_TARGET = 0.70  # 70% target success rate
    RESPONSE_TIME_LIMIT = 120  # seconds
    
    # Food Source Thresholds
    FOOD_SCORE_PREMIUM = 9.0  # Premium grade threshold
    FOOD_SCORE_HIGH = 7.0     # High grade threshold
    FOOD_SCORE_GOOD = 5.0     # Good grade threshold
    FOOD_SCORE_MODERATE = 3.0 # Moderate grade threshold
    
    # Redis Configuration (if using Replit's Redis)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"

settings = Settings()
