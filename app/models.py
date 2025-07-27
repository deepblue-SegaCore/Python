
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

# Enhanced Alert Model (Phase 2)
class EnhancedAlert(BaseModel):
    # From Pine Script
    version: str = "1.0"
    timestamp: datetime
    symbol: str
    exchange: str
    alert_type: str
    direction: SignalDirection
    strength: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    pressure: float = Field(..., ge=0)
    threshold: Optional[float] = Field(None, ge=0)
    
    # Food Source Assessment
    food_source: FoodSource
    
    # Phase 2 Enhancements
    environmental_state: Optional[EnvironmentalState] = None
    institutional_flow: Optional[Dict] = None
    correlation_data: Optional[Dict] = None
    ml_prediction: Optional[Dict] = None

# Pattern Memory Model
class Pattern(BaseModel):
    symbol: str
    timestamp: datetime
    environmental_state: Dict
    signal_strength: float
    confidence: float
    food_source: FoodSource
    outcome: Optional[float] = None
    success_probability: float = 0.5
    sample_count: int = 1
    decay_weight: float = 1.0
