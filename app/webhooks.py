
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
async def tradingview_webhook(request: Request, body: Any = Body(None)):
    """
    Main webhook endpoint for TradingView alerts
    Enhanced with Phase 2 Food Source Intelligence
    """
    try:
        # Initialize intelligence engine
        food_intel = FoodSourceIntelligence()
        
        # Get raw body for debugging
        raw_body = await request.body()
        content_type = request.headers.get("content-type", "")
        
        print(f"🔔 Webhook received - Content-Type: {content_type}")
        print(f"🔔 Raw body: {raw_body}")
        print(f"🔔 Parsed body: {body}")
        
        alert_data = {}
        
        # Handle different content types and formats
        if body is None and raw_body:
            # Try to parse raw body
            try:
                if content_type.startswith("application/json"):
                    alert_data = json.loads(raw_body.decode('utf-8'))
                else:
                    # Treat as plain text
                    alert_data = {"message": raw_body.decode('utf-8')}
            except (json.JSONDecodeError, UnicodeDecodeError):
                alert_data = {"message": "Invalid payload format"}
        elif isinstance(body, str):
            try:
                alert_data = json.loads(body)
            except json.JSONDecodeError:
                alert_data = {"message": body}
        elif isinstance(body, dict):
            alert_data = body
        elif body is None:
            alert_data = {"message": "Empty payload received"}
        else:
            alert_data = {"message": str(body)}
        
        # Ensure we have at least some default values
        if not alert_data or len(alert_data) == 0:
            alert_data = {
                "alert_type": "unknown",
                "symbol": "unknown", 
                "message": "Empty or invalid payload"
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

@router.post("/debug")
async def debug_webhook(request: Request, body: Any = Body(None)):
    """Debug endpoint to inspect incoming webhook requests"""
    raw_body = await request.body()
    headers = dict(request.headers)
    
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": headers,
        "raw_body": raw_body.decode('utf-8') if raw_body else None,
        "parsed_body": body,
        "content_type": headers.get("content-type"),
        "content_length": headers.get("content-length")
    }
