"""
Food Source Intelligence Module
Implements Phase 2 10-point granular scoring system
Based on Technical Specification Section 4
"""
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from app.models import FoodSource, FoodQuantity, FoodQuality, Sustainability

@dataclass
class FoodSourceAssessment:
    """
    Enhanced Food Source Assessment with 10-point scoring
    Based on Phase 2 specifications
    """
    quantity: str  # SMALL, MEDIUM, LARGE
    quality: str   # LOW, MEDIUM, HIGH
    score: float   # 0-10 granular score
    sustainability: str  # LIMITED, MODERATE, GOOD, EXCELLENT, EXCEPTIONAL
    predicted_duration: str  # 30min-2h, 2-6h, 6-12h, 12-24h, 24-72h
    confidence: float
    rationale: Dict[str, str]  # Explanation of scoring

class FoodSourceIntelligence:
    """
    Implements Technical Specification Section 4: Food Source Intelligence
    Enhanced with Phase 2 10-point granular scoring
    """

    def __init__(self):
        # Scoring weights from specification
        self.quantity_weights = {
            'volume_surge': 2.0,      # 0-2 points
            'volume_trend': 1.0,      # 0-1 point
            'institutional_hours': 1.0, # 0-1 point
            'range_expansion': 1.0     # 0-1 point
        }

        self.quality_weights = {
            'resistance_level': 2.0,   # 0-2 points
            'directional_consistency': 1.0,  # 0-1 point
            'institutional_participation': 1.0,  # 0-1 point
            'timing_quality': 1.0,     # 0-1 point
            'market_structure': 1.0    # 0-1 point
        }

    def assess_food_source(self, alert_data: Dict) -> FoodSourceAssessment:
        """
        Assess food source quality based on alert characteristics
        Uses biological intelligence principles
        """
        # Ensure alert_data is not None
        if not alert_data:
            alert_data = {}

        # Extract key metrics with defaults
        strength = alert_data.get("strength", 0.5)
        confidence = alert_data.get("confidence", 0.5)
        pressure = alert_data.get("pressure", 1.0)
        direction = alert_data.get("direction", "NEUTRAL")
        exchange = alert_data.get("exchange", "UNKNOWN")
        symbol = alert_data.get("symbol", "UNKNOWN")

        # Extract relevant data
        food_data = alert_data.get('food_source', {})

        # Calculate component scores
        quantity_score, quantity_details = self._calculate_quantity_score(alert_data)
        quality_score, quality_details = self._calculate_quality_score(alert_data)

        # Calculate 10-point granular score
        granular_score = self._calculate_granular_score(
            quantity_score, 
            quality_score,
            alert_data
        )

        # Determine classifications based on scores
        quantity = self._classify_quantity(quantity_score)
        quality = self._classify_quality(quality_score)
        sustainability = self._classify_sustainability(granular_score)
        duration = self._predict_duration(granular_score)

        # Build rationale
        rationale = {
            "quantity_factors": quantity_details,
            "quality_factors": quality_details,
            "score_calculation": f"Base: {quantity_score + quality_score}/10, Adjusted: {granular_score:.1f}/10",
            "grade": self._get_grade_description(granular_score)
        }

        return FoodSourceAssessment(
            quantity=quantity,
            quality=quality,
            score=round(granular_score, 1),
            sustainability=sustainability,
            predicted_duration=duration,
            confidence=alert_data.get('confidence', 0.5),
            rationale=rationale
        )

    def _calculate_quantity_score(self, alert_data: Dict) -> Tuple[int, str]:
        """Calculate food quantity score (0-5 points max)"""
        score = 0
        details = []

        # Volume surge contribution (0-2 points)
        volume_ratio = alert_data.get('volume_surge_ratio', 1.0)
        if volume_ratio > 1.5:
            score += 2
            details.append("Strong volume surge (2pts)")
        elif volume_ratio > 1.2:
            score += 1
            details.append("Moderate volume surge (1pt)")
        else:
            details.append("Normal volume (0pts)")

        # Volume trend contribution (0-1 point)
        volume_trend = alert_data.get('volume_trend_strength', 1.0)
        if volume_trend > 1.1:
            score += 1
            details.append("Accelerating volume (1pt)")
        else:
            details.append("Stable volume trend (0pts)")

        # Institutional hours (0-1 point)
        if alert_data.get('institutional_hours', False):
            score += 1
            details.append("Institutional hours (1pt)")
        else:
            details.append("Retail hours (0pts)")

        # Range expansion (0-1 point)
        range_expansion = alert_data.get('range_expansion', 1.0)
        if range_expansion > 1.2:
            score += 1
            details.append("Range expanding (1pt)")
        else:
            details.append("Normal range (0pts)")

        return score, ", ".join(details)

    def _calculate_quality_score(self, alert_data: Dict) -> Tuple[int, str]:
        """Calculate food quality score (0-6 points max)"""
        score = 0
        details = []

        # Resistance level (0-2 points)
        resistance = alert_data.get('resistance_level', 'NORMAL')
        if resistance == 'LIGHT':
            score += 2
            details.append("Light resistance (2pts)")
        elif resistance == 'NORMAL':
            score += 1
            details.append("Normal resistance (1pt)")
        else:
            details.append("Heavy resistance (0pts)")

        # Directional consistency (0-1 point)
        if alert_data.get('consistent_advancement', False) or \
           alert_data.get('consistent_decline', False):
            score += 1
            details.append("Directional consistency (1pt)")
        else:
            details.append("Choppy movement (0pts)")

        # Institutional participation (0-1 point)
        if alert_data.get('institutional_hours', False):
            score += 1
            details.append("Institutional timing (1pt)")
        else:
            details.append("Retail timing (0pts)")

        # Timing quality (0-1 point)
        if not alert_data.get('is_weekend_approach', False):
            score += 1
            details.append("Good timing (1pt)")
        else:
            details.append("Weekend approach (0pts)")

        # Market structure (0-1 point)
        structure = alert_data.get('market_structure', 'NORMAL')
        if structure != 'CONSTRAINED':
            score += 1
            details.append("Open structure (1pt)")
        else:
            details.append("Constrained structure (0pts)")

        return score, ", ".join(details)

    def _calculate_granular_score(self, quantity: int, quality: int, 
                                  alert_data: Dict) -> float:
        """
        Calculate 10-point granular score with environmental adjustments
        """
        # Base score (max 11 points scaled to 10)
        base_score = (quantity + quality) * 10 / 11

        # Environmental modifiers
        modifiers = 1.0

        # Emergency conditions reduce score
        if alert_data.get('alert_type') == 'EMERGENCY':
            modifiers *= 0.7

        # High confidence increases score
        confidence = alert_data.get('confidence', 0.5)
        if confidence > 0.8:
            modifiers *= 1.1
        elif confidence < 0.4:
            modifiers *= 0.9

        # Environmental pressure bonus
        pressure = alert_data.get('pressure', 1.0)
        threshold = alert_data.get('threshold', 1.5)
        if pressure > threshold * 1.5:
            modifiers *= 1.15  # Extreme pressure bonus
        elif pressure > threshold:
            modifiers *= 1.05  # Active pressure bonus

        # Apply modifiers
        final_score = base_score * modifiers

        # Ensure score stays within 0-10 range
        return min(10.0, max(0.0, final_score))

    def _classify_quantity(self, score: int) -> str:
        """Maps quantity score to classification"""
        if score >= 4:
            return "LARGE"
        elif score >= 2:
            return "MEDIUM"
        else:
            return "SMALL"

    def _classify_quality(self, score: int) -> str:
        """Maps quality score to classification"""
        if score >= 4:
            return "HIGH"
        elif score >= 2:
            return "MEDIUM"
        else:
            return "LOW"

    def _classify_sustainability(self, score: float) -> str:
        """
        Maps 10-point score to sustainability rating
        Based on Phase 2 specifications
        """
        if score >= 9:
            return "EXCEPTIONAL"
        elif score >= 7:
            return "EXCELLENT"
        elif score >= 5:
            return "GOOD"
        elif score >= 3:
            return "MODERATE"
        else:
            return "LIMITED"

    def _predict_duration(self, score: float) -> str:
        """
        Predicts food source duration based on score
        Based on Phase 2 specifications
        """
        if score >= 9:
            return "24-72h"
        elif score >= 7:
            return "12-24h"
        elif score >= 5:
            return "6-12h"
        elif score >= 3:
            return "2-6h"
        else:
            return "30min-2h"

    def _get_grade_description(self, score: float) -> str:
        """
        Returns human-readable grade description
        """
        if score >= 9:
            return "🥩 PREMIUM GRADE - Exceptional institutional-quality opportunity"
        elif score >= 7:
            return "🍖 HIGH GRADE - Excellent sustained opportunity"
        elif score >= 5:
            return "🥘 GOOD GRADE - Solid standard opportunity"
        elif score >= 3:
            return "🍞 MODERATE GRADE - Limited quick opportunity"
        else:
            return "🍿 LIMITED GRADE - Minimal scalp opportunity only"