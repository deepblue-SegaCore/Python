
"""
Amoeba Trading System Backend - Phase 2
Environmental Intelligence Processing Engine
Based on cellular biology principles
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv

# Import routers
from app.webhooks import router as webhook_router
from app.config import settings

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="Biological Intelligence Trading System",
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with your Netlify URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhook_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Amoeba Trading System",
        "version": settings.API_VERSION,
        "phase": "2 - Environmental Intelligence",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "webhook": "/api/v1/webhooks/tradingview",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
