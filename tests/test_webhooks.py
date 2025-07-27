
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_webhook_status():
    response = client.get("/api/v1/webhooks/status")
    assert response.status_code == 200
    assert response.json()["status"] == "active"

def test_tradingview_webhook():
    webhook_data = {
        "symbol": "BTCUSD",
        "action": "buy",
        "price": 50000.0,
        "quantity": 0.1,
        "message": "Test signal"
    }
    
    response = client.post("/api/v1/webhooks/tradingview", json=webhook_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
