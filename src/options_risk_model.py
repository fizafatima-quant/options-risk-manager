# options_risk_model.py
import math
from scipy.stats import norm

class OptionsRiskModel:
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call"):
        """
        Black-Scholes option pricing model with risk metrics.
        
        Parameters
        ----------
        S : float
            Spot price of the underlying
        K : float
            Strike price
        T : float
            Time to maturity (in years)
        r : float
            Risk-free interest rate
        sigma : float
            Volatility of the underlying
        option_type : str
            "call" or "put"
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()

    def d1(self) -> float:
        return (math.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (
            self.sigma * math.sqrt(self.T)
        )

    def d2(self) -> float:
        return self.d1() - self.sigma * math.sqrt(self.T)

    def call_price(self) -> float:
        d1 = self.d1()
        d2 = self.d2()
        return self.S * norm.cdf(d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(d2)

    def put_price(self) -> float:
        d1 = self.d1()
        d2 = self.d2()
        return self.K * math.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)

    def price(self) -> float:
        if self.option_type == "call":
            return self.call_price()
        elif self.option_type == "put":
            return self.put_price()
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    # ===== Greeks =====
    def delta(self) -> float:
        d1 = self.d1()
        if self.option_type == "call":
            return norm.cdf(d1)
        elif self.option_type == "put":
            return norm.cdf(d1) - 1

    def gamma(self) -> float:
        d1 = self.d1()
        return norm.pdf(d1) / (self.S * self.sigma * math.sqrt(self.T))

    def vega(self) -> float:
        d1 = self.d1()
        return self.S * norm.pdf(d1) * math.sqrt(self.T) / 100  # scaled per 1% vol

    def theta(self) -> float:
        d1 = self.d1()
        d2 = self.d2()
        first = - (self.S * norm.pdf(d1) * self.sigma) / (2 * math.sqrt(self.T))
        if self.option_type == "call":
            second = - self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(d2)
            return (first + second) / 365  # per day
        elif self.option_type == "put":
            second = self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(-d2)
            return (first + second) / 365  # per day

    def rho(self) -> float:
        d2 = self.d2()
        if self.option_type == "call":
            return self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(d2) / 100
        elif self.option_type == "put":
            return -self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(-d2) / 100
