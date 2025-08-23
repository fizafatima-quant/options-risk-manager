# src/data_fetcher.py
import yfinance as yf
import pandas as pd
from typing import List, Optional

class DataFetcher:
    """
    Fetch historical and options data for a given ticker using yfinance.
    """

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.asset = yf.Ticker(ticker)

    def get_historical_prices(self, period: str = "1y") -> pd.DataFrame:
        """
        Fetch historical OHLCV price data.
        :param period: '1y', '6mo', '1mo', etc.
        :return: DataFrame with Date, Open, High, Low, Close, Volume
        """
        df = self.asset.history(period=period)
        df.reset_index(inplace=True)
        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    def list_expiries(self) -> List[str]:
        """
        List available option expiries.
        """
        return self.asset.options

    def get_option_chain(self, expiry: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch option chain for a given expiry.
        If expiry is None, fetch the nearest expiry.
        """
        if expiry is None:
            expiry = self.asset.options[0]  # nearest expiry

        chain = self.asset.option_chain(expiry)
        calls = chain.calls.copy()
        puts = chain.puts.copy()

        calls['type'] = 'call'
        puts['type'] = 'put'

        return pd.concat([calls, puts], ignore_index=True)
