
# Amoeba Trading Backend

A FastAPI-based trading backend with TradingView webhook integration.

## Features

- FastAPI web framework
- TradingView webhook receiver
- Trade signal processing
- Health monitoring endpoints
- Structured logging
- Comprehensive testing

## API Endpoints

### Core Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check

### Webhook Endpoints
- `POST /api/v1/webhooks/tradingview` - Receive TradingView alerts
- `GET /api/v1/webhooks/status` - Check webhook status

## Webhook Payload Format

Send POST requests to `/api/v1/webhooks/tradingview` with the following JSON structure:

```json
{
    "symbol": "BTCUSD",
    "action": "buy",
    "price": 50000.0,
    "quantity": 0.1,
    "message": "Optional message"
}
```

## Configuration

Create a `.env` file based on `.env.example` to configure the application.

## Running the Application

1. Install dependencies: `pip install fastapi uvicorn pydantic`
2. Run the server: `python main.py`
3. Access the API at `http://localhost:5000`
4. View API docs at `http://localhost:5000/docs`

## Testing

Run tests with: `pytest tests/`

## Development

The application is structured as follows:
- `app/main.py` - FastAPI application setup
- `app/webhooks.py` - Webhook handling logic
- `app/models.py` - Pydantic data models
- `app/config.py` - Application configuration
- `tests/` - Test suite
