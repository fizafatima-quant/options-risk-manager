import json
from risk_metrics.margin import MarginCalculator
from market_data import get_market_data

# Load portfolio
with open('portfolio.json') as f:
    portfolio = json.load(f)

# Get live market data
underlying_price, volatility = get_market_data('AAPL')

# Initialize and run calculator
calculator = MarginCalculator(risk_free_rate=0.05)
margin = calculator.calculate_margin(
    positions=portfolio,
    underlying_price=underlying_price,
    volatility=volatility,
    stress_scenario=0.20  # Simulate a 20% volatility spike
)

# Print results
print(f"Required Margin: ${margin:,.2f}")

# Stress test: Market crash (-10% price, +50% volatility)
crash_price = underlying_price * 0.90
crash_vol = volatility * 1.50
crash_margin = calculator.calculate_margin(portfolio, crash_price, crash_vol)
print(f"Crash Scenario Margin: ${crash_margin:,.2f}")