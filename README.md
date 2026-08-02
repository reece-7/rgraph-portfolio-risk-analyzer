# rGraph — Portfolio Risk Analyzer

rGraph is an interactive portfolio analytics application built with Python and Streamlit.

It allows users to construct a custom portfolio, evaluate its historical performance, simulate future outcomes, compare allocation methods, analyze rebalancing strategies, measure transaction-cost drag, and study the portfolio's relationship with a market benchmark.

The project combines quantitative finance models with an interactive financial dashboard designed for practical portfolio analysis.

## Live Application

https://rgraph-portfolio.streamlit.app

> The public deployment will reflect the latest version after the `rgraph-v2` branch is merged into `main`.

---

## Core Capabilities

### Historical Performance

rGraph calculates and visualizes:

- Total return
- Annualized return
- Annualized volatility
- Sharpe Ratio
- Maximum drawdown
- Historical Value at Risk at 95%
- Historical Expected Shortfall at 95%
- Daily portfolio returns
- Historical portfolio value

### Monte Carlo Simulation

The application includes two simulation engines:

- Parametric Monte Carlo
- Historical bootstrap Monte Carlo

Users can configure either:

- A future target date
- A fixed number of simulated trading periods

Simulation outputs include:

- Median terminal value
- Mean terminal value
- Probability of loss
- Value at Risk
- Expected Shortfall
- Percentile fan charts
- Terminal-value distributions
- Parametric and bootstrap model comparison

### Portfolio Optimization

rGraph evaluates alternative portfolio constructions using:

- Random portfolio simulation
- Efficient Frontier analysis
- Maximum Sharpe portfolio
- Minimum-volatility portfolio
- Risk Parity allocation
- Current allocation versus Risk Parity
- Asset-level portfolio weights

### Rebalancing Analysis

The application compares:

- Buy and Hold
- Monthly rebalancing
- Quarterly rebalancing
- Annual rebalancing

It also models several transaction-cost assumptions and calculates:

- Final portfolio value
- Return and volatility
- Sharpe Ratio
- Maximum drawdown
- Total transaction costs
- Portfolio value lost to trading costs
- Cost drag by strategy

### Market Sensitivity

The portfolio is evaluated relative to a selected benchmark through:

- Beta
- Correlation
- Annualized active return
- Tracking Error
- Information Ratio
- Upside Capture
- Downside Capture
- Capture Ratio
- Rolling Beta
- Indexed portfolio-versus-benchmark performance

### Data Export

The dashboard provides downloadable CSV datasets for the main analytical outputs, including:

- Historical prices
- Asset returns
- Portfolio returns
- Portfolio values
- Performance summary
- Monte Carlo metrics
- Efficient Frontier
- Optimal portfolios
- Risk Parity weights
- Rebalancing results
- Transaction-cost analysis
- Market sensitivity
- Rolling Beta

---

## User Inputs

Users can configure:

| Category | Inputs |
|---|---|
| Portfolio | Tickers, weights and initial capital |
| Historical data | Start date and optional end date |
| Benchmark | Custom benchmark ticker |
| Simulation | Number of simulations and forecast horizon |
| Forecast mode | Target date or trading periods |
| Assumptions | Risk-free rate and trading days per year |

The application validates:

- Portfolio weights summing to 100%
- Positive asset weights
- Duplicate tickers
- Missing benchmark symbols
- Invalid or unavailable market data
- Insufficient historical observations
- Invalid simulation horizons

---

## Default Portfolio

The default configuration is:

| Asset | Weight |
|---|---:|
| SPY | 40% |
| QQQ | 30% |
| TLT | 20% |
| GLD | 10% |

This provides exposure to:

- Broad US equities
- Technology and growth equities
- Long-duration US Treasury bonds
- Gold

All tickers and weights can be replaced directly from the sidebar.

---

## Application Workflow

```text
Portfolio configuration
        ↓
Market-data download and validation
        ↓
Historical return calculation
        ↓
Performance and risk analysis
        ↓
Parametric Monte Carlo simulation
        ↓
Bootstrap Monte Carlo simulation
        ↓
Portfolio optimization
        ↓
Risk Parity allocation
        ↓
Rebalancing and transaction-cost analysis
        ↓
Benchmark sensitivity
        ↓
Interactive dashboard and CSV exports
Technology Stack

The application is built with:

Python
Streamlit
pandas
NumPy
SciPy
Altair
yfinance

Additional development and research tools include:

Jupyter
Matplotlib
Git
GitHub
Project Structure
rgraph-portfolio-risk-analyzer/
├── .streamlit/
│   └── config.toml
├── app.py
├── run_analysis.py
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    ├── data_loader.py
    ├── market_sensitivity.py
    ├── monte_carlo.py
    ├── portfolio_analyzer.py
    ├── portfolio_optimization.py
    ├── rebalancing.py
    ├── risk_metrics.py
    └── ui/
        ├── __init__.py
        ├── charts.py
        ├── downloads.py
        ├── home.py
        ├── market.py
        ├── monte_carlo.py
        ├── optimization.py
        ├── overview.py
        ├── performance.py
        ├── rebalancing.py
        ├── setup.py
        ├── sidebar.py
        ├── styles.py
        └── tables.py
Main Components
Component	Responsibility
app.py	Streamlit application orchestration and session state
portfolio_analyzer.py	Complete analytical pipeline
data_loader.py	Market-data download and validation
risk_metrics.py	Historical performance and risk calculations
monte_carlo.py	Parametric and bootstrap simulation engines
portfolio_optimization.py	Efficient Frontier and Risk Parity
rebalancing.py	Rebalancing and transaction-cost simulation
market_sensitivity.py	Benchmark and capture analysis
src/ui/	Dashboard sections, charts, tables and styling
Installation

Clone the repository:

git clone https://github.com/reece-7/rgraph-portfolio-risk-analyzer.git
cd rgraph-portfolio-risk-analyzer

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Activate it on macOS or Linux:

source .venv/bin/activate

Install the dependencies:

pip install -r requirements.txt
Run the Application

Start the Streamlit dashboard:

python -m streamlit run app.py

The application will normally be available at:

http://localhost:8501
Command-Line Analysis

The project also includes a non-interactive analysis script:

python run_analysis.py

This can be used to execute the analytical pipeline without the Streamlit interface.

Design and Engineering Features

The current version includes:

Modular analytical architecture
Independent UI modules
Session-state persistence
Cached portfolio analysis
Input-change detection
Multi-stage analysis status
Unified financial tables
Interactive Altair visualizations
Responsive dark financial interface
Clear validation and error handling
Downloadable analytical datasets
Methodology Notes

Historical performance metrics are estimated from downloaded market prices.

The parametric Monte Carlo model generates simulated returns using estimated historical statistical properties.

The bootstrap model resamples historical observations and therefore preserves more of the empirical return distribution.

Portfolio optimization is based on historical estimates of return, volatility and correlation.

Risk Parity follows a different objective from maximum-Sharpe and minimum-volatility optimization: it attempts to distribute portfolio risk more evenly across the selected assets.

Transaction-cost analysis applies modeled costs to trades created by each rebalancing strategy.

Limitations

The application relies on historical data and simplified quantitative assumptions.

Important limitations include:

Historical relationships may not persist
Monte Carlo results are scenario estimates, not forecasts
Return distributions may change through time
Liquidity, taxes and market impact are not fully modeled
Portfolio optimization is sensitive to estimated inputs
Long-horizon uncertainty increases materially

The application is intended for educational and analytical use and does not constitute financial advice.

Author

Ouyang Sun

GitHub: reece-7