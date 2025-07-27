"""
Data models for Amoeba Trading System
Based on Technical Specifications
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum

# Enums matching biological states
class EnvironmentalState(str, Enum):
    DORMANT = "DORMANT"
    WATCHING = "WATCHING"
    BUILDING = "BUILDING"
    ACTIVE = "ACTIVE"
    EXTREME = "EXTREME"

class SignalDirection(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

class FoodQuantity(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class FoodQuality(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Sustainability(str, Enum):
    LIMITED = "LIMITED"
    MODERATE = "MODERATE"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"
    EXCEPTIONAL = "EXCEPTIONAL"

# Food Source Model
class FoodSource(BaseModel):
    quantity: FoodQuantity
    quality: FoodQuality
    sustainability: Sustainability
    predicted_duration: str = Field(..., pattern="^\\d+-\\d+h$")
    score: Optional[float] = Field(None, ge=0, le=10)

class EnhancedAlert(BaseModel):
    """Enhanced alert model for Phase 2 Environmental Intelligence"""
    alert_type: str
    symbol: str
    exchange: Optional[str] = None
    direction: Optional[str] = None
    strength: Optional[float] = None
    confidence: Optional[float] = None
    pressure: Optional[float] = None
    timestamp: Optional[str] = None
    version: Optional[str] = "1.0"
    message: Optional[str] = None

class WebhookResponse(BaseModel):
    """Standard webhook response model"""
    status: str
    message: str
    alert_type: Optional[str] = None
    symbol: Optional[str] = None
    timestamp: str = datetime.utcnow().isoformat()