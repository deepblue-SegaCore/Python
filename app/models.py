
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ActionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    CLOSE = "close"

class WebhookData(BaseModel):
    symbol: str
    action: ActionType
    price: float
    quantity: Optional[float] = 1.0
    timestamp: Optional[datetime] = None
    message: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class TradeSignal(BaseModel):
    symbol: str
    action: ActionType
    price: float
    quantity: float
    timestamp: Optional[datetime] = None
    processed_at: datetime = datetime.now()
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class TradeResponse(BaseModel):
    status: str
    message: str
    trade_id: Optional[str] = None
    signal: Optional[TradeSignal] = None
