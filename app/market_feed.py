
"""
Market Data Feed Module - Simplified Version
Feeds simulated market data to existing Amoeba intelligence
"""
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List
import random

class MarketDataFeed:
    """
    Simulated market data feed for testing (without ccxt dependency)
    """
    
    def __init__(self, food_intel, learning_system, websocket_manager):
        # Use YOUR existing intelligence modules!
        self.food_intel = food_intel
        self.learning_system = learning_system
        self.websocket_manager = websocket_manager
        
        # Symbol configurations
        self.symbols = {
            'BTCUSD': 'BTC/USDT',
            'ETHUSD': 'ETH/USDT',
            'BNBUSD': 'BNB/USDT',
            'SOLUSD': 'SOL/USDT'
        }
        
        # Base prices for simulation
        self.base_prices = {
            'BTCUSD': 45000,
            'ETHUSD': 2800,
            'BNBUSD': 310,
            'SOLUSD': 85
        }
        
    async def start_continuous_feed(self):
        """
        Continuously generate simulated market data and process through existing intelligence
        """
        print("🌊 Starting simulated market data feed...")
        
        while True:
            for display_symbol, exchange_symbol in self.symbols.items():
                try:
                    # Generate simulated market data
                    market_data = await self.generate_simulated_data(display_symbol)
                    
                    # Process through YOUR existing intelligence!
                    assessment = self.food_intel.assess_food_source(market_data)
                    
                    # Process through YOUR pattern learning
                    learning_result = self.learning_system.process_new_signal(
                        display_symbol, 
                        market_data
                    )
                    
                    # Prepare broadcast data
                    broadcast_data = {
                        "type": "market_update",
                        "symbol": display_symbol,
                        "environmental_pressure": market_data['pressure'],
                        "threshold": market_data['threshold'],
                        "direction": market_data['direction'],
                        "food_source": {
                            "score": assessment.score,
                            "grade": assessment.rationale["grade"],
                            "quantity": assessment.quantity,
                            "quality": assessment.quality,
                            "sustainability": assessment.sustainability,
                            "predicted_duration": assessment.predicted_duration
                        },
                        "pattern_learning": {
                            "enhanced_confidence": learning_result['enhanced_confidence'],
                            "recommendation": learning_result['learning_recommendation']
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    # Broadcast to dashboard
                    await self.websocket_manager.broadcast(broadcast_data)
                    
                except Exception as e:
                    print(f"Error processing {display_symbol}: {e}")
                    
            # Update every 10 seconds (slower for simulation)
            await asyncio.sleep(10)
    
    async def generate_simulated_data(self, symbol: str) -> Dict:
        """
        Generate realistic simulated market data
        """
        base_price = self.base_prices[symbol]
        
        # Generate realistic price movement
        price_change = random.uniform(-0.05, 0.05)  # ±5% movement
        current_price = base_price * (1 + price_change)
        
        # Generate volume and volatility
        volume = random.uniform(1000000, 5000000)
        volatility_pressure = random.uniform(0.5, 3.0)
        volume_pressure = random.uniform(0.8, 2.5)
        environmental_pressure = (volatility_pressure + volume_pressure) / 2
        
        # Generate RSI-like indicator
        rsi_value = random.uniform(20, 80)
        
        # Determine direction
        if rsi_value > 60:
            direction = "BULLISH"
        elif rsi_value < 40:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"
        
        # Format data for your existing intelligence modules
        return {
            'symbol': symbol,
            'exchange': 'SIMULATED',
            'price': float(current_price),
            'volume': float(volume),
            'pressure': float(environmental_pressure),
            'threshold': 1.8,  # Your default
            'direction': direction,
            'strength': float(environmental_pressure / 1.8),  # Relative to threshold
            'confidence': random.uniform(0.5, 0.9),  # Simulated confidence
            'volume_surge_ratio': float(volume_pressure),
            'volume_trend_strength': 1.0,
            'institutional_hours': self.is_institutional_hours(),
            'range_expansion': 1.0,
            'resistance_level': 'NORMAL',
            'market_structure': 'NORMAL',
            'consistent_advancement': random.choice([True, False]),
            'consistent_decline': random.choice([True, False]),
            'is_weekend_approach': False
        }
    
    def is_institutional_hours(self) -> bool:
        """Check if current time is institutional trading hours"""
        hour = datetime.utcnow().hour
        return 7 <= hour <= 22  # London + NY sessions
