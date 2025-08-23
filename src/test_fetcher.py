from data_fetcher import DataFetcher

fetcher = DataFetcher("AAPL")

# Historical prices
prices = fetcher.get_historical_prices("6mo")
print(prices.head())

# Option chain
options = fetcher.get_option_chain()
print(options.head())

# Expiries
print(fetcher.list_expiries())
