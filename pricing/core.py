from math import log, sqrt, exp
from scipy.stats import norm

def black_scholes(S: float, K: float, T: float, r: float, 
                 sigma: float, option_type: str = 'call') -> dict:
    """
    Calculate option price and Greeks (delta, vega).
    Args:
        S: Spot price
        K: Strike price
        T: Time to expiry (in years)
        r: Risk-free rate
        sigma: Volatility
        option_type: 'call' or 'put'
    Returns:
        Dictionary with 'price', 'delta', and 'vega'
    """
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    else:
        price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = -norm.cdf(-d1)
    
    # Calculate vega (same for calls/puts)
    vega = S * norm.pdf(d1) * sqrt(T)  # norm.pdf = probability density function
    
    return {
        'price': round(price, 4),
        'delta': round(delta, 4),
        'vega': round(vega, 4)
    }