
from fastapi import FastAPI
from app.webhooks import router as webhooks_router
from app.config import settings

app = FastAPI(
    title="Amoeba Trading Backend",
    description="Trading backend with TradingView webhook integration",
    version="1.0.0"
)

# Include routers
app.include_router(webhooks_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Amoeba Trading Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
