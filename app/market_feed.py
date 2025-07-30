
"""
Market Data Feed Module - Real Market Data via Binance API
Feeds real-time market data to existing Amoeba intelligence using Binance public API
"""
import asyncio
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List
import ssl

class MarketDataFeed:
    """
    Real market data feed using Binance public API (no API key needed)
    """
    
    def __init__(self, food_intel, learning_system, websocket_manager):
        # Use YOUR existing intelligence modules!
        self.food_intel = food_intel
        self.learning_system = learning_system
        self.websocket_manager = websocket_manager
        
        # Symbol configurations - using Binance format
        self.symbols = {
            'BTCUSD': 'BTCUSDT',
            'ETHUSD': 'ETHUSDT', 
            'BNBUSD': 'BNBUSDT',
            'SOLUSD': 'SOLUSDT',
            'ADAUSD': 'ADAUSDT',
            'DOTUSD': 'DOTUSDT'
        }
        
        # Binance API endpoints
        self.binance_base = "https://api.binance.com/api/v3"
        
        # Create SSL context that doesn't verify certificates (for API calls)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
    async def start_continuous_feed(self):
        """
        Continuously fetch real market data and process through existing intelligence
        """
        print("🌊 Starting REAL market data feed via Binance API...")
        
        while True:
            for display_symbol, binance_symbol in self.symbols.items():
                try:
                    # Fetch real market data
                    market_data = await self.fetch_binance_data(display_symbol, binance_symbol)
                    
                    if market_data:
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
                            "price": market_data['price'],
                            "price_change_24h": market_data.get('price_change_24h', 0),
                            "volume_24h": market_data.get('volume', 0),
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
                            "data_source": "Binance API",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        
                        # Broadcast to dashboard
                        await self.websocket_manager.broadcast(broadcast_data)
                        
                        print(f"📈 {display_symbol}: ${market_data['price']:.2f} | "
                              f"24h: {market_data.get('price_change_24h', 0):.2f}% | "
                              f"Vol: ${market_data.get('volume', 0):,.0f} | "
                              f"Score: {assessment.score}/10")
                        
                except Exception as e:
                    print(f"❌ Error fetching {display_symbol}: {e}")
                    
            # Update every 10 seconds (Binance allows much higher rates)
            await asyncio.sleep(10)
    
    async def fetch_binance_data(self, symbol: str, binance_symbol: str) -> Dict:
        """
        Fetch real market data from Binance public API
        """
        try:
            # Get 24hr ticker statistics from Binance
            ticker_url = f"{self.binance_base}/ticker/24hr?symbol={binance_symbol}"
            
            # Make HTTP request
            ticker_data = await self.make_api_request(ticker_url)
            
            if not ticker_data:
                return None
                
            current_price = float(ticker_data['lastPrice'])
            price_change_24h = float(ticker_data['priceChangePercent'])
            volume_24h = float(ticker_data['volume']) * current_price  # Convert to USD volume
            
            # Calculate environmental pressure based on real data
            volatility_pressure = abs(price_change_24h) / 10.0  # Normalize percentage change
            volume_pressure = min(volume_24h / 1000000000, 3.0)  # Volume in billions, capped at 3.0
            environmental_pressure = (volatility_pressure + volume_pressure) / 2
            
            # Determine direction based on 24h change
            if price_change_24h > 2:
                direction = "BULLISH"
            elif price_change_24h < -2:
                direction = "BEARISH"
            else:
                direction = "NEUTRAL"
            
            # Format data for your existing intelligence modules
            return {
                'symbol': symbol,
                'exchange': 'Binance',
                'price': float(current_price),
                'volume': float(volume_24h),
                'price_change_24h': float(price_change_24h),
                'pressure': float(environmental_pressure),
                'threshold': 1.8,  # Your default
                'direction': direction,
                'strength': float(environmental_pressure / 1.8),  # Relative to threshold
                'confidence': min(0.9, 0.5 + abs(price_change_24h) / 20),  # Higher confidence with bigger moves
                'volume_surge_ratio': float(min(volume_pressure, 2.0)),
                'volume_trend_strength': 1.0,
                'institutional_hours': self.is_institutional_hours(),
                'range_expansion': 1.0 + abs(price_change_24h) / 100,
                'resistance_level': 'HIGH' if abs(price_change_24h) > 5 else 'NORMAL',
                'market_structure': 'TRENDING' if abs(price_change_24h) > 3 else 'NORMAL',
                'consistent_advancement': price_change_24h > 1,
                'consistent_decline': price_change_24h < -1,
                'is_weekend_approach': False,
                # Additional Binance-specific data
                'high_24h': float(ticker_data['highPrice']),
                'low_24h': float(ticker_data['lowPrice']),
                'open_price': float(ticker_data['openPrice']),
                'trade_count': int(ticker_data['count']),
                'quote_volume': float(ticker_data['quoteVolume'])
            }
            
        except Exception as e:
            print(f"❌ Binance API Error for {symbol}: {e}")
            return None
    
    async def make_api_request(self, url: str) -> Dict:
        """
        Make HTTP API request using urllib (no external dependencies)
        """
        try:
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (compatible; AmoebaTrading/2.0)')
            
            # Run in thread to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: urllib.request.urlopen(request, context=self.ssl_context, timeout=10)
            )
            
            data = response.read().decode('utf-8')
            return json.loads(data)
            
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"⚠️  Rate limit hit, waiting...")
                await asyncio.sleep(5)  # Wait 5 seconds on rate limit
            else:
                print(f"❌ HTTP Error: {e.code} - {e.reason}")
            return None
        except urllib.error.URLError as e:
            print(f"❌ URL Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Request Error: {e}")
            return None
    
    def is_institutional_hours(self) -> bool:
        """Check if current time is institutional trading hours"""
        hour = datetime.utcnow().hour
        return 7 <= hour <= 22  # London + NY sessions
