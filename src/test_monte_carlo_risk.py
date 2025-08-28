# test_monte_carlo_risk.py
from portfolio_manager import PortfolioManager
from monte_carlo_risk import MonteCarloRisk

def test_mc_simulation_stats():
    pm = PortfolioManager()
    pm.add_position(S=100, K=100, T=1.0, r=0.03, sigma=0.2, option_type="call", quantity=10)

    mc = MonteCarloRisk(pm)
    stats = mc.simulate(n_sims=2000, horizon=0.5, seed=42)

    assert "mean" in stats
    assert "VaR_95" in stats
    assert stats["std"] > 0
    assert stats["VaR_99"] <= stats["VaR_95"]
