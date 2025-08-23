import math
from scipy.stats import norm

def d1(S, K, T, r, sigma):
    return (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * math.sqrt(T)

def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    """Black-Scholes price for a European call or put option."""
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)

    if option_type == "call":
        return S * norm.cdf(D1) - K * math.exp(-r * T) * norm.cdf(D2)
    elif option_type == "put":
        return K * math.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def delta(S, K, T, r, sigma, option_type="call"):
    D1 = d1(S, K, T, r, sigma)
    if option_type == "call":
        return norm.cdf(D1)
    elif option_type == "put":
        return norm.cdf(D1) - 1

def gamma(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return norm.pdf(D1) / (S * sigma * math.sqrt(T))

def vega(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return S * norm.pdf(D1) * math.sqrt(T)

def theta(S, K, T, r, sigma, option_type="call"):
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    first = -(S * norm.pdf(D1) * sigma) / (2 * math.sqrt(T))
    if option_type == "call":
        return first - r * K * math.exp(-r * T) * norm.cdf(D2)
    elif option_type == "put":
        return first + r * K * math.exp(-r * T) * norm.cdf(-D2)

def rho(S, K, T, r, sigma, option_type="call"):
    D2 = d2(S, K, T, r, sigma)
    if option_type == "call":
        return K * T * math.exp(-r * T) * norm.cdf(D2)
    elif option_type == "put":
        return -K * T * math.exp(-r * T) * norm.cdf(-D2)
