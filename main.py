
"""
Amoeba Trading System Backend - Phase 2
Environmental Intelligence Processing Engine with WebSocket Support
Based on cellular biology principles
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import asyncio
from typing import List
import os
from dotenv import load_dotenv

# Import routers
from app.webhooks import router as webhook_router
from app.config import settings

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="Biological Intelligence Trading System with WebSocket Support",
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🔌 WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"🔌 WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if self.active_connections:
            message_str = json.dumps(message)
            print(f"📡 Broadcasting to {len(self.active_connections)} clients: {message.get('type', 'unknown')}")
            
            # Remove disconnected clients
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_str)
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Include routers
app.include_router(webhook_router, prefix="/api/v1")

# WebSocket endpoint for real-time signals
@app.websocket("/ws/signals")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            
            # Echo back a confirmation
            await manager.send_personal_message(
                json.dumps({
                    "type": "connection_confirmed",
                    "message": "WebSocket connection active",
                    "timestamp": datetime.utcnow().isoformat()
                }),
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "websocket_connections": len(manager.active_connections)
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Amoeba Trading System",
        "version": settings.API_VERSION,
        "phase": "2 - Environmental Intelligence with WebSocket",
        "status": "operational",
        "websocket_connections": len(manager.active_connections),
        "endpoints": {
            "health": "/health",
            "webhook": "/api/v1/webhooks/tradingview",
            "websocket": "/ws/signals",
            "docs": "/docs"
        }
    }

# Function to broadcast signals (used by webhook handler)
async def broadcast_signal(signal_data: dict):
    """Broadcast trading signal to all WebSocket clients"""
    await manager.broadcast({
        "type": "trading_signal",
        "data": signal_data,
        "timestamp": datetime.utcnow().isoformat()
    })

# Make manager available to other modules
app.state.websocket_manager = manager

if __name__ == "__main__":
    import uvicorn
    print("🌱 Starting Amoeba Trading System Backend...")
    print("🔌 WebSocket endpoint: ws://localhost:5000/ws/signals")
    print("🌐 API endpoint: http://localhost:5000/api/v1/alerts")
    print("📚 Documentation: http://localhost:5000/docs")
    uvicorn.run(app, host="0.0.0.0", port=5000)
