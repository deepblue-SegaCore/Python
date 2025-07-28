
"""
Pattern Memory System - 95-minute biological memory
Implements associative learning without external database
Based on Technical Specification Section 3.2
"""
import json
import time
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import threading

@dataclass
class MemoryPattern:
    """
    Individual pattern with biological decay
    """
    pattern_id: str
    symbol: str
    timestamp: datetime
    environmental_state: Dict
    signal_strength: float
    confidence: float
    food_source: Dict
    outcome: Optional[float] = None
    success_probability: float = 0.5
    sample_count: int = 1
    
    def calculate_decay_weight(self) -> float:
        """
        Calculate exponential decay based on age
        Biological limit: 95 minutes
        """
        age_minutes = (datetime.utcnow() - self.timestamp).total_seconds() / 60
        if age_minutes >= 95:
            return 0.0
        return math.exp(-age_minutes / 95)
    
    def is_expired(self) -> bool:
        """Check if pattern has exceeded biological memory limit"""
        age_minutes = (datetime.utcnow() - self.timestamp).total_seconds() / 60
        return age_minutes >= 95

@dataclass
class PatternMemoryBank:
    """
    In-memory pattern storage with automatic expiry
    Mimics biological 95-minute memory constraint
    """
    patterns: Dict[str, List[MemoryPattern]] = field(default_factory=lambda: defaultdict(list))
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _cleanup_interval: int = 300  # 5 minutes
    _last_cleanup: datetime = field(default_factory=datetime.utcnow)
    
    def store_pattern(self, symbol: str, pattern_data: Dict) -> str:
        """
        Store a new pattern with automatic expiry tracking
        """
        with self._lock:
            # Create pattern ID
            pattern_id = f"{symbol}_{int(time.time()*1000)}"
            
            # Create memory pattern
            pattern = MemoryPattern(
                pattern_id=pattern_id,
                symbol=symbol,
                timestamp=datetime.utcnow(),
                environmental_state=pattern_data.get('environmental_state', {}),
                signal_strength=pattern_data.get('signal_strength', 0),
                confidence=pattern_data.get('confidence', 0),
                food_source=pattern_data.get('food_source', {}),
                outcome=pattern_data.get('outcome'),
                success_probability=pattern_data.get('success_probability', 0.5),
                sample_count=1
            )
            
            # Store pattern
            self.patterns[symbol].append(pattern)
            
            # Periodic cleanup
            self._cleanup_expired_patterns()
            
            print(f"Pattern stored: {pattern_id} for {symbol}")
            return pattern_id
    
    def get_similar_patterns(self, symbol: str, current_state: Dict, 
                           similarity_threshold: float = 0.7) -> List[Tuple[MemoryPattern, float]]:
        """
        Find patterns similar to current state within memory window
        Returns patterns with their similarity scores and decay weights
        """
        with self._lock:
            similar_patterns = []
            
            # Clean up first
            self._cleanup_expired_patterns()
            
            # Search through symbol's patterns
            for pattern in self.patterns.get(symbol, []):
                if pattern.is_expired():
                    continue
                    
                # Calculate similarity
                similarity = self._calculate_similarity(current_state, pattern.environmental_state)
                
                if similarity >= similarity_threshold:
                    decay_weight = pattern.calculate_decay_weight()
                    relevance = similarity * decay_weight
                    
                    similar_patterns.append((pattern, relevance))
            
            # Sort by relevance (similarity * decay_weight)
            similar_patterns.sort(key=lambda x: x[1], reverse=True)
            
            return similar_patterns[:10]  # Return top 10 most relevant
    
    def update_pattern_outcome(self, pattern_id: str, outcome: float) -> bool:
        """
        Update pattern with learning outcome
        Implements biological associative learning
        """
        with self._lock:
            for symbol_patterns in self.patterns.values():
                for pattern in symbol_patterns:
                    if pattern.pattern_id == pattern_id and not pattern.is_expired():
                        # Biological learning rate
                        learning_rate = 0.1
                        
                        # Update success probability
                        old_prob = pattern.success_probability
                        new_prob = old_prob + learning_rate * (outcome - old_prob)
                        pattern.success_probability = min(1.0, max(0.0, new_prob))
                        
                        # Update outcome and sample count
                        pattern.outcome = outcome
                        pattern.sample_count += 1
                        
                        print(f"Pattern {pattern_id} updated: probability {old_prob:.2f} -> {new_prob:.2f}")
                        return True
            
            return False
    
    def get_pattern_statistics(self, symbol: str) -> Dict:
        """
        Get learning statistics for a symbol
        """
        with self._lock:
            self._cleanup_expired_patterns()
            
            patterns = self.patterns.get(symbol, [])
            active_patterns = [p for p in patterns if not p.is_expired()]
            
            if not active_patterns:
                return {
                    "total_patterns": 0,
                    "average_success_rate": 0,
                    "high_confidence_patterns": 0,
                    "memory_utilization": 0
                }
            
            success_rates = [p.success_probability for p in active_patterns]
            high_confidence = sum(1 for p in active_patterns if p.success_probability > 0.7)
            
            # Calculate memory utilization (how fresh are patterns)
            avg_decay = sum(p.calculate_decay_weight() for p in active_patterns) / len(active_patterns)
            
            return {
                "total_patterns": len(active_patterns),
                "average_success_rate": sum(success_rates) / len(success_rates),
                "high_confidence_patterns": high_confidence,
                "memory_utilization": avg_decay,
                "oldest_pattern_age": max((datetime.utcnow() - p.timestamp).total_seconds() / 60 
                                         for p in active_patterns) if active_patterns else 0
            }
    
    def _calculate_similarity(self, state1: Dict, state2: Dict) -> float:
        """
        Calculate similarity between two environmental states
        Returns value between 0 and 1
        """
        # Key features for comparison
        features = [
            'pressure', 'momentum', 'volume_surge', 'trend',
            'signal_strength', 'confidence', 'market_structure'
        ]
        
        similarities = []
        
        for feature in features:
            val1 = state1.get(feature)
            val2 = state2.get(feature)
            
            if val1 is None or val2 is None:
                continue
                
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Numerical similarity
                if val1 == 0 and val2 == 0:
                    similarities.append(1.0)
                else:
                    max_val = max(abs(val1), abs(val2))
                    if max_val > 0:
                        similarities.append(1 - abs(val1 - val2) / max_val)
            elif val1 == val2:
                # Exact match for strings/booleans
                similarities.append(1.0)
            else:
                similarities.append(0.0)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _cleanup_expired_patterns(self):
        """
        Remove patterns that exceed biological memory limit
        """
        now = datetime.utcnow()
        
        # Only cleanup every interval
        if (now - self._last_cleanup).total_seconds() < self._cleanup_interval:
            return
            
        self._last_cleanup = now
        
        # Remove expired patterns
        for symbol in list(self.patterns.keys()):
            self.patterns[symbol] = [
                p for p in self.patterns[symbol] 
                if not p.is_expired()
            ]
            
            # Remove symbol if no patterns left
            if not self.patterns[symbol]:
                del self.patterns[symbol]
        
        print(f"Memory cleanup completed. Active symbols: {len(self.patterns)}")

# Global memory instance
pattern_memory = PatternMemoryBank()

class AssociativeLearning:
    """
    Implements biological associative learning
    Links environmental patterns with outcomes
    """
    
    def __init__(self):
        self.learning_rate = 0.1  # Biological learning rate
        self.success_threshold = 0.7  # Target 70% success (biological range)
        
    def process_new_signal(self, symbol: str, signal_data: Dict) -> Dict:
        """
        Process new signal with pattern matching and learning
        """
        # Extract environmental state
        environmental_state = {
            'pressure': signal_data.get('pressure', 0),
            'momentum': signal_data.get('direction'),
            'volume_surge': signal_data.get('volume_surge_ratio', 1),
            'signal_strength': signal_data.get('strength', 0),
            'confidence': signal_data.get('confidence', 0),
            'market_structure': signal_data.get('market_structure', 'NORMAL')
        }
        
        # Find similar historical patterns
        similar_patterns = pattern_memory.get_similar_patterns(
            symbol, 
            environmental_state
        )
        
        # Calculate learning-enhanced confidence
        enhanced_confidence = self._calculate_enhanced_confidence(
            signal_data.get('confidence', 0.5),
            similar_patterns
        )
        
        # Store this pattern for future learning
        pattern_id = pattern_memory.store_pattern(symbol, {
            'environmental_state': environmental_state,
            'signal_strength': signal_data.get('strength', 0),
            'confidence': signal_data.get('confidence', 0),
            'food_source': signal_data.get('food_source', {}),
            'success_probability': enhanced_confidence
        })
        
        # Get pattern statistics
        stats = pattern_memory.get_pattern_statistics(symbol)
        
        return {
            'pattern_id': pattern_id,
            'enhanced_confidence': enhanced_confidence,
            'similar_patterns_found': len(similar_patterns),
            'pattern_statistics': stats,
            'learning_recommendation': self._get_learning_recommendation(
                enhanced_confidence,
                stats
            )
        }
    
    def _calculate_enhanced_confidence(self, base_confidence: float, 
                                     similar_patterns: List[Tuple[MemoryPattern, float]]) -> float:
        """
        Enhance confidence based on historical pattern success
        """
        if not similar_patterns:
            return base_confidence
            
        # Weight success probabilities by relevance
        weighted_sum = 0
        total_weight = 0
        
        for pattern, relevance in similar_patterns[:5]:  # Top 5 patterns
            weighted_sum += pattern.success_probability * relevance
            total_weight += relevance
            
        if total_weight > 0:
            historical_confidence = weighted_sum / total_weight
            # Blend with base confidence
            return 0.6 * base_confidence + 0.4 * historical_confidence
        
        return base_confidence
    
    def _get_learning_recommendation(self, confidence: float, stats: Dict) -> str:
        """
        Provide recommendation based on learning state
        """
        if stats['total_patterns'] < 10:
            return "LEARNING: Gathering patterns - trade cautiously"
        elif stats['average_success_rate'] > 0.7:
            if confidence > 0.7:
                return "HIGH CONFIDENCE: Historical patterns support this signal"
            else:
                return "MIXED: Good history but weak current signal"
        elif stats['average_success_rate'] < 0.4:
            return "CAUTION: Poor historical performance in similar conditions"
        else:
            return "MODERATE: Continue monitoring pattern effectiveness"

# Create global learning instance
learning_system = AssociativeLearning()
