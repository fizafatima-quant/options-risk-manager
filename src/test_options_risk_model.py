import pytest
from options_risk_model import black_scholes_price, delta, gamma, vega, theta, rho

def test_call_price():
    price = black_scholes_price(100, 100, 1, 0.05, 0.2, "call")
    assert round(price, 2) == 10.45  # known benchmark

def test_put_price():
    price = black_scholes_price(100, 100, 1, 0.05, 0.2, "put")
    assert round(price, 2) == 5.57  # known benchmark

def test_greeks():
    d = delta(100, 100, 1, 0.05, 0.2, "call")
    g = gamma(100, 100, 1, 0.05, 0.2)
    v = vega(100, 100, 1, 0.05, 0.2)
    t = theta(100, 100, 1, 0.05, 0.2, "call")
    r = rho(100, 100, 1, 0.05, 0.2, "call")

    assert 0 < d < 1
    assert g > 0
    assert v > 0
    assert t < 0
    assert r > 0
