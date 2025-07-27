from math import log, sqrt, exp
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    else:
        price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = -norm.cdf(-d1)
    
    return {'price': price, 'delta': delta}