# src/portfolio_manager.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
from options_risk_model import OptionsRiskModel

@dataclass
class Position:
    S: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: str  # "call" or "put"
    quantity: int     # + for long, - for short

    def model(self) -> OptionsRiskModel:
        return OptionsRiskModel(self.S, self.K, self.T, self.r, self.sigma, self.option_type)

class PortfolioManager:
    """Tracks multiple option positions and aggregates value + Greeks."""
    def __init__(self) -> None:
        self.positions: List[Position] = []

    def add_position(self, S: float, K: float, T: float, r: float, sigma: float,
                     option_type: str, quantity: int) -> None:
        self.positions.append(Position(S, K, T, r, sigma, option_type, quantity))

    def portfolio_value(self) -> float:
        return sum(p.model().price() * p.quantity for p in self.positions)

    def portfolio_greeks(self) -> Dict[str, float]:
        totals = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
        for p in self.positions:
            m = p.model()
            q = p.quantity
            totals["delta"] += m.delta() * q
            totals["gamma"] += m.gamma() * q
            totals["vega"]  += m.vega()  * q
            totals["theta"] += m.theta() * q
            totals["rho"]   += m.rho()   * q
        return totals

    def scenario_shift(self, dS: float = 0.0, dVol: float = 0.0, dR: float = 0.0) -> Dict[str, float]:
        """Return value after a scenario shift in underlying, vol, or rate."""
        shifted_value = 0.0
        for p in self.positions:
            m = OptionsRiskModel(
                S=p.S + dS,
                K=p.K,
                T=p.T,
                r=p.r + dR,
                sigma=max(1e-6, p.sigma + dVol),
                option_type=p.option_type
            )
            shifted_value += m.price() * p.quantity
        return {
            "base_value": self.portfolio_value(),
            "shifted_value": shifted_value,
            "pnl": shifted_value - self.portfolio_value(),
        }
