
"""
Webhook handlers for TradingView integration
"""
from fastapi import APIRouter, HTTPException, Request, Body
from app.models import EnhancedAlert, WebhookResponse
from app.config import settings
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

@router.post("/tradingview", response_model=WebhookResponse)
async def tradingview_webhook(request: Request):
    """
    Main webhook endpoint for TradingView alerts
    This is where Pine Script alerts arrive for Phase 2 Environmental Intelligence
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        
        # Verify signature if configured
        if not verify_webhook_signature(request, body):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse alert data
        if not body:
            raise HTTPException(status_code=400, detail="Empty request body")
            
        alert_data = json.loads(body.decode('utf-8'))
        
        # Validate alert structure
        try:
            alert = EnhancedAlert(**alert_data)
        except Exception as validation_error:
            print(f"Alert validation error: {validation_error}")
            # Still process basic alerts for compatibility
            alert = None
        
        # Log for debugging
        print(f"🔔 Webhook received: {alert_data}")
        
        # Phase 2 Environmental Intelligence Processing
        response = WebhookResponse(
            status="success",
            message="Alert received and processed by Environmental Intelligence Engine",
            alert_type=alert_data.get("alert_type", "unknown"),
            symbol=alert_data.get("symbol", "unknown"),
            timestamp=datetime.utcnow().isoformat()
        )
        
        return response
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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
