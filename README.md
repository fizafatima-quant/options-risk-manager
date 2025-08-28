Options Risk Manager 📊

A Python-based toolkit for options analysis, portfolio management, and risk assessment. Designed for real-world applicability, it covers option pricing, Greeks calculation, portfolio aggregation, scenario analysis, and Monte Carlo risk simulation.

🔹 Features
1. Data Fetcher

Fetch historical price data and option chains for any ticker using yfinance.

Supports:

Historical prices (OHLC + Volume)

Option chains for nearest or specific expiries

Example:

from data_fetcher import DataFetcher

df_prices = DataFetcher("AAPL").get_historical_prices(period="1y")
option_chain = DataFetcher("AAPL").get_option_chain()

2. Option Pricing Model

Implements Black-Scholes model for:

Call and Put pricing

Greeks: Delta, Gamma, Vega, Theta, Rho

Fully tested with pytest.

3. Portfolio Manager

Aggregate multiple option positions.

Compute:

Portfolio value

Portfolio Greeks

Run scenario analyses for changes in:

Underlying price

Volatility

Interest rates

Example:

pm.add_position(S=100, K=100, T=1, r=0.03, sigma=0.2, option_type="call", quantity=10)
pm.portfolio_value()
pm.scenario_shift(dS=5, dVol=0.05, dR=0.01)

4. Portfolio Risk Visualization

Interactive visualizations for portfolio exposure and risk metrics.

Identify high-risk positions and correlations between option positions.

5. Monte Carlo Risk Simulation

Perform Monte Carlo simulations to model portfolio risk under stochastic market scenarios.

Compute statistical measures (mean, std, percentiles) of portfolio value.

Example:

from monte_carlo_risk import MonteCarloRisk

mc = MonteCarloRisk(portfolio)
mc.run_simulation(num_simulations=10000)
mc.results_summary()

🔹 Project Structure
src/
├── data_fetcher.py           # Fetch historical and option data
├── options_risk_model.py     # Black-Scholes pricing & Greeks
├── portfolio_manager.py      # Portfolio aggregation & scenario analysis
├── risk_analysis.py          # Stress testing & risk metrics
├── monte_carlo_risk.py       # Monte Carlo simulations
├── tests/                    # Pytest unit tests

🔹 Tools & Libraries

Python 3.13

pandas, numpy

yfinance

matplotlib / seaborn (for visualizations)

pytest (for testing)

🔹 How to Run

Clone the repository:

git clone https://github.com/fizafatima-quant/options-risk-manager.git
cd options-risk-manager


Install dependencies:

python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt


Run tests:

pytest -v


Run any script from src/ to fetch data, price options, or simulate portfolio risk.
