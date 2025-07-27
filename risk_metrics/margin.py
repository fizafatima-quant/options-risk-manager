from pricing.core import black_scholes

def portfolio_margin(positions, S=100, r=0.05, sigma=0.3):
    total = 0
    for p in positions:
        greeks = black_scholes(
            S=S,
            K=p['strike'],
            T=p['days_to_expiry']/365,
            r=r,
            sigma=sigma
        )
        total += abs(greeks['delta']) * p['quantity'] * 100 * 0.15
    return total