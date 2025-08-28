from typing import List, Dict
from dataclasses import dataclass
from options_risk_model import OptionsRiskModel

@dataclass
class Position:
    S: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: str
    quantity: int

    def model(self) -> OptionsRiskModel:
        return OptionsRiskModel(
            S=self.S,
            K=self.K,
            T=self.T,
            r=self.r,
            sigma=self.sigma,
            option_type=self.option_type
        )

class PortfolioManager:
    def __init__(self):
        self.positions: List[Position] = []

    def add_position(self, S, K, T, r, sigma, option_type, quantity):
        self.positions.append(
            Position(S, K, T, r, sigma, option_type, quantity)
        )

    def portfolio_value(self) -> float:
        total = 0.0
        for p in self.positions:
            total += p.model().price() * p.quantity
        return total

    def portfolio_greeks(self) -> Dict[str, float]:
        totals = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
        for p in self.positions:
            m = p.model()
            q = p.quantity
            totals["delta"] += m.delta() * q
            totals["gamma"] += m.gamma() * q
            totals["vega"] += m.vega() * q
            totals["theta"] += m.theta() * q
            totals["rho"] += m.rho() * q
        return totals

    def scenario_shift(self, dS=0.0, dSigma=0.0, dR=0.0) -> Dict[str, float]:
        """Shift market inputs and recalc portfolio greeks."""
        totals = {"value": 0.0, "delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
        for p in self.positions:
            stressed_model = OptionsRiskModel(
                S=p.S + dS,
                K=p.K,
                T=p.T,
                r=p.r + dR,
                sigma=p.sigma + dSigma,
                option_type=p.option_type
            )
            q = p.quantity
            totals["value"] += stressed_model.price() * q
            totals["delta"] += stressed_model.delta() * q
            totals["gamma"] += stressed_model.gamma() * q
            totals["vega"] += stressed_model.vega() * q
            totals["theta"] += stressed_model.theta() * q
            totals["rho"] += stressed_model.rho() * q
        return totals

    def stress_test(self, dS=0.0, dSigma=0.0, dR=0.0) -> Dict[str, float]:
        """
        Perform a simple stress test by shifting S, sigma, and r for all positions.
        """
        totals = {"value": 0.0, "delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}

        for p in self.positions:
            stressed_model = OptionsRiskModel(
                S=p.S + dS,
                K=p.K,
                T=p.T,
                r=p.r + dR,
                sigma=p.sigma + dSigma,
                option_type=p.option_type
            )
            q = p.quantity
            totals["value"] += stressed_model.price() * q
            totals["delta"] += stressed_model.delta() * q
            totals["gamma"] += stressed_model.gamma() * q
            totals["vega"] += stressed_model.vega() * q
            totals["theta"] += stressed_model.theta() * q
            totals["rho"] += stressed_model.rho() * q

        return totals
