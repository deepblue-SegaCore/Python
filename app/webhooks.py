
"""
Webhook handlers for TradingView integration
"""
from fastapi import APIRouter, HTTPException, Request, Body
from app.models import EnhancedAlert, WebhookResponse
from app.config import settings
from app.intelligence import FoodSourceIntelligence, FoodSourceAssessment
from typing import Dict, Any
import json
import hmac
import hashlib
from datetime import datetime

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

def verify_webhook_signature(request: Request, body: bytes) -> bool:
    """Verify webhook authenticity if secret is configured"""
    if not settings.WEBHOOK_SECRET:
        return True
        
    signature = request.headers.get("X-Webhook-Signature")
    if not signature:
        return False
        
    expected = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)

@router.post("/tradingview")
async def tradingview_webhook(request: Request, body: Dict[str, Any] = Body(...)):
    """
    Main webhook endpoint for TradingView alerts
    Enhanced with Phase 2 Food Source Intelligence
    """
    try:
        # Initialize intelligence engine
        food_intel = FoodSourceIntelligence()
        
        # Log for debugging
        print(f"🔔 Webhook received: {body}")
        
        # Basic validation
        if body is None:
            raise HTTPException(status_code=400, detail="Empty request body")
        
        # Extract key fields - handle both dict and string formats
        if isinstance(body, str):
            try:
                alert_data = json.loads(body)
            except json.JSONDecodeError:
                alert_data = {"message": body}
        else:
            alert_data = body
        
        # Ensure we have at least some default values for empty payloads
        if not alert_data:
            alert_data = {
                "alert_type": "unknown",
                "symbol": "unknown",
                "message": "Empty payload received"
            }
        
        # Perform food source assessment
        assessment = food_intel.assess_food_source(alert_data)
        
        # Process alert with enhanced intelligence
        response = {
            "status": "success",
            "message": "Alert received and processed with Phase 2 intelligence",
            "alert_type": alert_data.get("alert_type", "unknown"),
            "symbol": alert_data.get("symbol", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "food_source_assessment": {
                "score": assessment.score,
                "grade": assessment.rationale["grade"],
                "sustainability": assessment.sustainability,
                "predicted_duration": assessment.predicted_duration,
                "quantity": assessment.quantity,
                "quality": assessment.quality,
                "confidence": assessment.confidence,
                "details": assessment.rationale
            }
        }
        
        # Log the assessment
        print(f"🍯 Food Source Assessment: Score={assessment.score}/10, "
              f"Sustainability={assessment.sustainability}, "
              f"Duration={assessment.predicted_duration}")
        
        return response
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def webhook_status():
    """Check webhook system status"""
    return {
        "status": "active",
        "version": settings.API_VERSION,
        "phase": "2 - Environmental Intelligence",
        "webhook_secret_configured": bool(settings.WEBHOOK_SECRET)
    }

@router.get("/test")
async def test_webhook():
    """Test endpoint to verify webhook routing"""
    return {
        "message": "Webhook router is working",
        "endpoint": "/api/v1/webhooks/tradingview",
        "status": "ready"
    }
