# monte_carlo_risk.py
import numpy as np
from typing import List, Dict
from portfolio_manager import PortfolioManager

class MonteCarloRisk:
    def __init__(self, portfolio: PortfolioManager):
        self.portfolio = portfolio

    def simulate(self, n_sims: int = 10000, horizon: float = 1.0, seed: int = None) -> Dict[str, float]:
        """
        Monte Carlo simulation of portfolio value distribution.
        """
        if seed is not None:
            np.random.seed(seed)

        base_positions = self.portfolio.positions
        results = []

        for _ in range(n_sims):
            shifted_portfolio = PortfolioManager()
            for p in base_positions:
                # Simulate a shifted underlying price with GBM assumption
                S_new = p.S * np.exp((p.r - 0.5 * p.sigma**2) * horizon +
                                     p.sigma * np.sqrt(horizon) * np.random.normal())
                shifted_portfolio.add_position(S=S_new, K=p.K, T=p.T - horizon, r=p.r,
                                               sigma=p.sigma, option_type=p.option_type,
                                               quantity=p.quantity)
            results.append(shifted_portfolio.portfolio_value())

        results = np.array(results)
        return {
            "mean": np.mean(results),
            "std": np.std(results),
            "VaR_95": np.percentile(results, 5),
            "VaR_99": np.percentile(results, 1),
        }
