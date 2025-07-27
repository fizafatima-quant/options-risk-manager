import matplotlib.pyplot as plt
from pricing.core import black_scholes
from market_data import get_market_data
import json

# Load portfolio
with open('portfolio.json') as f:
    portfolio = json.load(f)

# Get market data
underlying_price, volatility = get_market_data('AAPL')

# Calculate Greeks
deltas, vegas = [], []
for p in portfolio:
    greeks = black_scholes(
        S=underlying_price,
        K=p['strike'],
        T=p['days_to_expiry']/365,
        r=0.05,
        sigma=volatility,
        option_type=p['type']
    )
    deltas.append(greeks['delta'] * p['quantity'])
    vegas.append(greeks['vega'] * p['quantity'])

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.bar([f"Position {i+1}" for i in range(len(deltas))], deltas, color='blue')
ax1.set_title("Delta Exposure")
ax2.bar([f"Position {i+1}" for i in range(len(vegas))], vegas, color='red')
ax2.set_title("Vega Exposure")
plt.savefig('risk_exposure.png')  # Save the plot
plt.show()