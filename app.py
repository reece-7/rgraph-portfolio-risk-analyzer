import pandas as pd
import streamlit as st

from src.portfolio_analyzer import analyze_portfolio
from src.ui.home import render_home
from src.ui.sidebar import render_sidebar
from src.ui.overview import render_overview
from src.ui.monte_carlo import render_monte_carlo
from src.ui.optimization import render_optimization
from src.ui.rebalancing import render_rebalancing
from src.ui.market import render_market
from src.ui.downloads import render_downloads
from src.ui.performance import render_performance
from src.ui.styles import apply_global_styles
from src.ui.setup import render_portfolio_setup

st.set_page_config(
    page_title="rGraph | Portfolio Risk Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_global_styles()

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "analysis_inputs" not in st.session_state:
    st.session_state.analysis_inputs = None


@st.cache_data(
    ttl=3600,
    max_entries=3,
    show_spinner=False
)
def get_cached_analysis(
    tickers,
    weights_items,
    start_date,
    initial_value,
    n_simulations,
    time_horizon,
    trading_days,
    risk_free_rate,
    benchmark_ticker
):
    weights = dict(weights_items)

    return analyze_portfolio(
        tickers=list(tickers),
        weights=weights,
        start_date=start_date,
        end_date=None,
        initial_value=initial_value,
        n_simulations=n_simulations,
        time_horizon=time_horizon,
        trading_days=trading_days,
        risk_free_rate=risk_free_rate,
        benchmark_ticker=benchmark_ticker,
        transaction_cost_rates={
            "0.00%": 0.0000,
            "0.05%": 0.0005,
            "0.10%": 0.0010,
            "0.25%": 0.0025
        }
    )


render_home()

sidebar_inputs = render_sidebar()

initial_value = sidebar_inputs["initial_value"]
start_date = sidebar_inputs["start_date"]
benchmark_ticker = sidebar_inputs["benchmark_ticker"]
n_simulations = sidebar_inputs["n_simulations"]
fan_chart_lines = sidebar_inputs["fan_chart_lines"]
time_horizon = sidebar_inputs["time_horizon"]
risk_free_rate = sidebar_inputs["risk_free_rate"]
trading_days = sidebar_inputs["trading_days"]
tickers = sidebar_inputs["tickers"]
weights_percent = sidebar_inputs["weights_percent"]

portfolio_inputs = [
    (ticker, weight / 100)
    for ticker, weight in zip(tickers, weights_percent)
    if ticker
]

valid_tickers = [
    ticker
    for ticker, _ in portfolio_inputs
]

weights = {
    ticker: weight
    for ticker, weight in portfolio_inputs
}

weight_sum = sum(
    weight
    for _, weight in portfolio_inputs
)

duplicate_tickers = (
    len(valid_tickers) != len(set(valid_tickers))
)

non_positive_weight_tickers = [
    ticker
    for ticker, weight in portfolio_inputs
    if weight <= 0
]

# =========================
# PORTFOLIO SETUP
# =========================

run_button = render_portfolio_setup(
    portfolio_inputs=portfolio_inputs,
    weight_sum=weight_sum,
    duplicate_tickers=duplicate_tickers,
    non_positive_weight_tickers=non_positive_weight_tickers,
    benchmark_ticker=benchmark_ticker,
)

# =========================
# CALCULATE NEW ANALYSIS
# =========================

if run_button:
    if abs(weight_sum - 1.0) > 0.0001:
        st.error(
            "Cannot run analysis: weights must sum to 100%."
        )

    elif len(valid_tickers) < 2:
        st.error(
            "Cannot run analysis: please enter at least two valid tickers."
        )

    elif duplicate_tickers:
        st.error(
            "Cannot run analysis: duplicate tickers are not allowed."
        )

    elif non_positive_weight_tickers:
        st.error(
            "Cannot run analysis: all selected assets must have "
            "a positive weight."
        )

    elif benchmark_ticker == "":
        st.error(
            "Cannot run analysis: benchmark ticker cannot be empty."
        )

    else:
        with st.spinner("Running portfolio analysis..."):
            try:
                results = get_cached_analysis(
                    tickers=tuple(valid_tickers),
                    weights_items=tuple(sorted(weights.items())),
                    start_date=str(start_date),
                    initial_value=float(initial_value),
                    n_simulations=int(n_simulations),
                    time_horizon=int(time_horizon),
                    trading_days=int(trading_days),
                    risk_free_rate=float(risk_free_rate),
                    benchmark_ticker=benchmark_ticker,
                )

                st.session_state.analysis_results = results

                st.session_state.analysis_inputs = {
                    "tickers": valid_tickers,
                    "weights": weights,
                    "initial_value": float(initial_value),
                    "start_date": str(start_date),
                    "benchmark_ticker": benchmark_ticker,
                    "n_simulations": int(n_simulations),
                    "time_horizon": int(time_horizon),
                    "trading_days": int(trading_days),
                    "risk_free_rate": float(risk_free_rate),
                }

                st.success(
                    "Analysis completed successfully."
                )

            except ValueError as error:
                st.error("Input or data error.")
                st.warning(str(error))

            except KeyError as error:
                st.error(
                    "Ticker or benchmark data could not be found."
                )

                st.warning(
                    "Please check that all tickers and the benchmark "
                    "are valid and available on Yahoo Finance."
                )

                st.exception(error)

            except Exception as error:
                st.error(
                    "An unexpected error occurred while running "
                    "the analysis."
                )

                st.warning(
                    "Please check your tickers, weights, internet "
                    "connection, and selected date range."
                )

                st.exception(error)


# =========================
# LOAD SAVED ANALYSIS
# =========================

results = st.session_state.analysis_results
analysis_inputs = st.session_state.analysis_inputs


if results is None or analysis_inputs is None:
    st.html(
        """
        <div class="rg-dashboard-empty">
            <span class="rg-dashboard-empty-line"></span>

            <span>
                No analysis has been generated yet.
                Use the current allocation to unlock the dashboard.
            </span>
        </div>
        """
    )

    st.stop()


# =========================
# PREPARE SAVED INPUTS
# =========================

analyzed_initial_value = analysis_inputs["initial_value"]

analyzed_benchmark_ticker = (
    analysis_inputs["benchmark_ticker"]
)

analyzed_n_simulations = (
    analysis_inputs["n_simulations"]
)

analyzed_weights = analysis_inputs["weights"]


analyzed_setup_df = pd.DataFrame(
    list(analyzed_weights.items()),
    columns=["Ticker", "Weight"],
)

analyzed_setup_df["Weight (%)"] = (
    analyzed_setup_df["Weight"] * 100
)


risk_parity_df = results[
    "risk_parity_weights"
].to_frame(
    name="Weight"
)

risk_parity_df["Weight (%)"] = (
    risk_parity_df["Weight"] * 100
)


st.caption(
    "Dashboard results refer to the latest completed analysis."
)


# =========================
# DASHBOARD TABS
# =========================

(
    tab_overview,
    tab_performance,
    tab_monte_carlo,
    tab_optimization,
    tab_rebalancing,
    tab_market,
    tab_downloads,
) = st.tabs(
    [
        "Overview",
        "Performance",
        "Monte Carlo",
        "Optimization",
        "Rebalancing",
        "Market Sensitivity",
        "Downloads",
    ]
)


with tab_overview:
    render_overview(
        results=results,
        initial_value=analyzed_initial_value,
        setup_df=analyzed_setup_df,
    )


with tab_performance:
    render_performance(
        results=results,
    )


with tab_monte_carlo:
    render_monte_carlo(
        results=results,
        fan_chart_lines=fan_chart_lines,
        n_simulations=analyzed_n_simulations,
    )


with tab_optimization:
    render_optimization(
        results=results,
        risk_parity_df=risk_parity_df,
    )


with tab_rebalancing:
    render_rebalancing(
        results=results,
    )


with tab_market:
    render_market(
        results=results,
        benchmark_ticker=analyzed_benchmark_ticker,
    )


with tab_downloads:
    render_downloads(
        results=results,
    )