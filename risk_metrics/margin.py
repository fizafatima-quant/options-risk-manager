from pricing.core import black_scholes
from typing import List, Dict

class MarginCalculator:
    """Professional margin calculator with stress testing."""
    def __init__(self, risk_free_rate: float = 0.05):
        self.risk_free_rate = risk_free_rate
    
    def calculate_margin(self, 
                       positions: List[Dict], 
                       underlying_price: float,
                       volatility: float = 0.3,
                       stress_scenario: float = 0.0) -> float:
        """
        Calculate margin with volatility shocks.
        Args:
            positions: List of dicts with keys: 'type', 'strike', 'quantity', 'days_to_expiry'
            stress_scenario: Volatility shock (e.g., 0.20 = +20%)
        """
        total_margin = 0
        for p in positions:
            greeks = black_scholes(
                S=underlying_price,
                K=p['strike'],
                T=p['days_to_expiry']/365,
                r=self.risk_free_rate,
                sigma=volatility + stress_scenario,
                option_type=p['type']
            )
            # SPAN-like margin rule: 15% of delta-adjusted notional
            total_margin += abs(greeks['delta']) * p['quantity'] * underlying_price * 0.15
        return round(total_margin, 2)