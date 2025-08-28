# src/test_portfolio_manager.py
from portfolio_manager import PortfolioManager

def test_portfolio_aggregation():
    pm = PortfolioManager()
    # long 10 calls ATM
    pm.add_position(S=100, K=100, T=1.0, r=0.03, sigma=0.2, option_type="call", quantity=10)
    # short 5 puts OTM
    pm.add_position(S=100, K=90, T=1.0, r=0.03, sigma=0.2, option_type="put", quantity=-5)

    value = pm.portfolio_value()
    greeks = pm.portfolio_greeks()

    assert value != 0
    assert isinstance(greeks, dict)
    for k in ["delta", "gamma", "vega", "theta", "rho"]:
        assert k in greeks

def test_scenario_shift():
    pm = PortfolioManager()
    pm.add_position(S=100, K=100, T=1.0, r=0.03, sigma=0.2, option_type="call", quantity=1)

    res = pm.scenario_shift(dS=5.0, dVol=0.05, dR=0.01)
    assert "base_value" in res and "shifted_value" in res and "pnl" in res
