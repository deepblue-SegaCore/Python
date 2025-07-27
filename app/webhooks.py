
from fastapi import APIRouter, HTTPException, Request
from app.models import WebhookData, TradeSignal
import logging

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/webhooks/tradingview")
async def receive_tradingview_webhook(webhook_data: WebhookData):
    """
    Receive and process TradingView webhook alerts
    """
    try:
        logger.info(f"Received webhook: {webhook_data.dict()}")
        
        # Process the webhook data
        trade_signal = TradeSignal(
            symbol=webhook_data.symbol,
            action=webhook_data.action,
            price=webhook_data.price,
            quantity=webhook_data.quantity,
            timestamp=webhook_data.timestamp
        )
        
        # Here you would implement your trading logic
        # For now, we'll just log the signal
        logger.info(f"Processed trade signal: {trade_signal.dict()}")
        
        return {
            "status": "success",
            "message": "Webhook received and processed",
            "signal": trade_signal.dict()
        }
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

@router.get("/webhooks/status")
async def webhook_status():
    """
    Check webhook endpoint status
    """
    return {"status": "active", "endpoint": "/api/v1/webhooks/tradingview"}
