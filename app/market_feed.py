
"""
Market Data Feed Module - Real Market Data
Feeds real-time market data to existing Amoeba intelligence using free APIs
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
    Real market data feed using free APIs (no external dependencies)
    """
    
    def __init__(self, food_intel, learning_system, websocket_manager):
        # Use YOUR existing intelligence modules!
        self.food_intel = food_intel
        self.learning_system = learning_system
        self.websocket_manager = websocket_manager
        
        # Symbol configurations - using CoinGecko API format
        self.symbols = {
            'BTCUSD': 'bitcoin',
            'ETHUSD': 'ethereum', 
            'BNBUSD': 'binancecoin',
            'SOLUSD': 'solana'
        }
        
        # API endpoints
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.binance_base = "https://api.binance.com/api/v3"
        
        # Create SSL context that doesn't verify certificates (for API calls)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
    async def start_continuous_feed(self):
        """
        Continuously fetch real market data and process through existing intelligence
        """
        print("🌊 Starting REAL market data feed...")
        
        while True:
            for display_symbol, coin_id in self.symbols.items():
                try:
                    # Fetch real market data
                    market_data = await self.fetch_real_market_data(display_symbol, coin_id)
                    
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
                            "data_source": "CoinGecko API",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        
                        # Broadcast to dashboard
                        await self.websocket_manager.broadcast(broadcast_data)
                        
                        print(f"📈 {display_symbol}: ${market_data['price']:.2f} | "
                              f"24h: {market_data.get('price_change_24h', 0):.2f}% | "
                              f"Score: {assessment.score}/10")
                        
                except Exception as e:
                    print(f"❌ Error fetching {display_symbol}: {e}")
                    
            # Update every 30 seconds (respecting API rate limits)
            await asyncio.sleep(30)
    
    async def fetch_real_market_data(self, symbol: str, coin_id: str) -> Dict:
        """
        Fetch real market data from CoinGecko API
        """
        try:
            # Fetch price data from CoinGecko
            price_url = f"{self.coingecko_base}/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
            
            # Make HTTP request
            price_data = await self.make_api_request(price_url)
            
            if not price_data or coin_id not in price_data:
                return None
                
            coin_data = price_data[coin_id]
            current_price = coin_data['usd']
            price_change_24h = coin_data.get('usd_24h_change', 0)
            volume_24h = coin_data.get('usd_24h_vol', 0)
            
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
                'exchange': 'CoinGecko',
                'price': float(current_price),
                'volume': float(volume_24h) if volume_24h else 1000000,
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
                'is_weekend_approach': False
            }
            
        except Exception as e:
            print(f"❌ API Error for {symbol}: {e}")
            return None
    
    async def make_api_request(self, url: str) -> Dict:
        """
        Make HTTP API request using urllib (no external dependencies)
        """
        try:
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (compatible; AmoebaTrading/1.0)')
            
            # Run in thread to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: urllib.request.urlopen(request, context=self.ssl_context, timeout=10)
            )
            
            data = response.read().decode('utf-8')
            return json.loads(data)
            
        except urllib.error.HTTPError as e:
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
