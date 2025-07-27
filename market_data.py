import yfinance as yf
from math import sqrt

def get_market_data(ticker: str) -> tuple:
    """Fetch live price and volatility for a stock."""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")  # 1 month of historical data
    price = hist['Close'].iloc[-1]  # Latest closing price
    volatility = hist['Close'].pct_change().std() * sqrt(252)  # Annualized volatility
    return price, volatility

# Example: Get data for Apple (AAPL)
underlying_price, volatility = get_market_data('AAPL')
print(f"AAPL Price: ${underlying_price:.2f}")
print(f"Implied Volatility: {volatility:.2%}")