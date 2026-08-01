import pandas as pd
import streamlit as st

from src.portfolio_analyzer import analyze_portfolio
from src.ui.home import render_home
from src.ui.sidebar import render_sidebar

st.set_page_config(
    page_title="rGraph | Portfolio Risk Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "analysis_inputs" not in st.session_state:
    st.session_state.analysis_inputs = None


@st.cache_data(
    ttl=3600,
    max_entries=30,
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
    if ticker != ""
]

valid_tickers = [ticker for ticker, weight in portfolio_inputs]

weights = {
    ticker: weight
    for ticker, weight in portfolio_inputs
}

weight_sum = sum(weight for ticker, weight in portfolio_inputs)

duplicate_tickers = len(valid_tickers) != len(set(valid_tickers))

non_positive_weight_tickers = [
    ticker for ticker, weight in portfolio_inputs
    if weight <= 0
]

weight_sum = sum(weights.values())
valid_tickers = list(weights.keys())
duplicate_tickers = len(valid_tickers) != len(set(valid_tickers))


# =========================
# PORTFOLIO SETUP
# =========================

st.subheader("Portfolio Setup")

setup_df = pd.DataFrame({
    "Ticker": valid_tickers,
    "Weight": list(weights.values())
})

if not setup_df.empty:
    setup_df["Weight (%)"] = setup_df["Weight"] * 100
    st.dataframe(setup_df[["Ticker", "Weight (%)"]], use_container_width=True)

st.write(f"Total weight: **{weight_sum * 100:.2f}%**")

if abs(weight_sum - 1.0) > 0.0001:
    st.warning("Portfolio weights must sum to 100% before running the analysis.")

if len(weights) < 2:
    st.warning("Please enter at least two valid tickers.")

if duplicate_tickers:
    st.warning("Duplicate tickers detected. Please use each ticker only once.")

if non_positive_weight_tickers:
    st.warning(
        "Some tickers have a weight of 0%. Please remove them or assign a positive weight."
    )

if benchmark_ticker == "":
    st.warning("Please enter a valid benchmark ticker.")


# =========================
# HELPER FUNCTION
# =========================

def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=True).encode("utf-8")

def build_fan_chart(paths_df, fan_chart_lines):
    """
    Builds a Monte Carlo fan chart with selected percentile bands.
    """

    if fan_chart_lines == 1:
        return pd.DataFrame({
            "Median": paths_df.quantile(0.50, axis=1)
        })

    if fan_chart_lines == 3:
        return pd.DataFrame({
            "25th Percentile": paths_df.quantile(0.25, axis=1),
            "Median": paths_df.quantile(0.50, axis=1),
            "75th Percentile": paths_df.quantile(0.75, axis=1)
        })

    return pd.DataFrame({
        "5th Percentile": paths_df.quantile(0.05, axis=1),
        "25th Percentile": paths_df.quantile(0.25, axis=1),
        "Median": paths_df.quantile(0.50, axis=1),
        "75th Percentile": paths_df.quantile(0.75, axis=1),
        "95th Percentile": paths_df.quantile(0.95, axis=1)
    })

# =========================
# RUN ANALYSIS
# =========================

run_button = st.button("Run Portfolio Analysis")

if run_button:
    if abs(weight_sum - 1.0) > 0.0001:
        st.error("Cannot run analysis: weights must sum to 100%.")
    elif len(weights) < 2:
        st.error("Cannot run analysis: please enter at least two valid tickers.")
    elif duplicate_tickers:
        st.error("Cannot run analysis: duplicate tickers are not allowed.")
    elif non_positive_weight_tickers:
        st.error("Cannot run analysis: all selected assets must have a positive weight.")
    elif benchmark_ticker == "":
        st.error("Cannot run analysis: benchmark ticker cannot be empty.")
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
                    benchmark_ticker=benchmark_ticker
                )

                st.session_state.analysis_results = results

                st.session_state.analysis_inputs = {
                    "tickers": valid_tickers,
                    "weights": weights,
                    "initial_value": initial_value,
                    "start_date": str(start_date),
                    "benchmark_ticker": benchmark_ticker,
                    "n_simulations": int(n_simulations),
                    "time_horizon": int(time_horizon),
                    "trading_days": int(trading_days),
                    "risk_free_rate": risk_free_rate
                }

                st.success("Analysis completed successfully.")

                performance_summary = pd.DataFrame(
                    [results["performance_summary"]],
                    index=["Custom Portfolio"]
                )

                monte_carlo_final_values = pd.DataFrame({
                    "Parametric Monte Carlo": results["parametric_final_values"],
                    "Bootstrap Monte Carlo": results["bootstrap_final_values"]
                })

                risk_parity_df = results["risk_parity_weights"].to_frame(
                    name="Weight"
                )
                risk_parity_df["Weight (%)"] = risk_parity_df["Weight"] * 100

                # =========================
                # TABS
                # =========================

                tab_overview, tab_performance, tab_monte_carlo, tab_optimization, tab_rebalancing, tab_market, tab_downloads = st.tabs(
                    [
                        "Overview",
                        "Performance",
                        "Monte Carlo",
                        "Optimization",
                        "Rebalancing",
                        "Market Sensitivity",
                        "Downloads"
                    ]
                )

                # =========================
                # OVERVIEW TAB
                # =========================

                with tab_overview:
                    st.header("Overview")

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric(
                        "Initial Capital",
                        f"{initial_value:,.2f}"
                    )

                    col2.metric(
                        "Final Value",
                        f"{results['performance_summary']['Final Value']:,.2f}"
                    )

                    col3.metric(
                        "Total Return",
                        f"{results['performance_summary']['Total Return'] * 100:.2f}%"
                    )

                    col4.metric(
                        "Sharpe Ratio",
                        f"{results['performance_summary']['Sharpe Ratio']:.2f}"
                    )

                    st.subheader("Portfolio Allocation")
                    allocation_df = setup_df[["Ticker", "Weight (%)"]].set_index("Ticker")
                    st.bar_chart(allocation_df)

                    st.subheader("Portfolio Value Over Time")
                    st.line_chart(results["portfolio_values"])

                # =========================
                # PERFORMANCE TAB
                # =========================

                with tab_performance:
                    st.header("Performance Summary")

                    st.dataframe(
                        performance_summary,
                        use_container_width=True
                    )

                    st.subheader("Portfolio Value Over Time")
                    st.line_chart(results["portfolio_values"])

                    st.subheader("Daily Portfolio Returns")
                    st.line_chart(results["portfolio_returns"])

                # =========================
                # MONTE CARLO TAB
                # =========================

                with tab_monte_carlo:
                    st.header("Monte Carlo Simulation")

                    st.subheader("Monte Carlo Risk Metrics")
                    st.dataframe(
                        results["monte_carlo_comparison"],
                        use_container_width=True
                    )

                    st.subheader("Final Value Distribution Summary")
                    st.dataframe(
                        monte_carlo_final_values.describe(),
                        use_container_width=True
                    )

                    parametric_paths_df = pd.DataFrame(results["parametric_paths"])
                    bootstrap_paths_df = pd.DataFrame(results["bootstrap_paths"])

                    st.subheader("Parametric Monte Carlo Fan Chart")

                    parametric_fan_chart = build_fan_chart(
                        parametric_paths_df,
                        fan_chart_lines
                    )

                    st.line_chart(parametric_fan_chart)

                    st.caption(
                        f"The fan chart displays {fan_chart_lines} percentile line(s). "
                        "The analysis still uses the full number of Monte Carlo simulations."
                    )

                    st.subheader("Bootstrap Monte Carlo Fan Chart")

                    bootstrap_fan_chart = build_fan_chart(
                        bootstrap_paths_df,
                        fan_chart_lines
                    )

                    st.line_chart(bootstrap_fan_chart)

                    st.caption(
                        f"The Bootstrap fan chart displays {fan_chart_lines} percentile line(s). "
                        "The analysis still uses the full number of Monte Carlo simulations."
                    )

                    st.subheader("Monte Carlo Final Values")
                    st.line_chart(monte_carlo_final_values)

                # =========================
                # OPTIMIZATION TAB
                # =========================

                with tab_optimization:
                    st.header("Portfolio Optimization")

                    st.subheader("Optimal Portfolios")
                    st.dataframe(
                        results["optimal_portfolios"],
                        use_container_width=True
                    )

                    st.subheader("Risk Parity Weights")
                    st.dataframe(
                        risk_parity_df,
                        use_container_width=True
                    )

                    st.subheader("Risk Parity Allocation")
                    st.bar_chart(risk_parity_df[["Weight (%)"]])

                    st.subheader("Efficient Frontier Sample")
                    st.dataframe(
                        results["efficient_frontier"].head(100),
                        use_container_width=True
                    )

                    st.scatter_chart(
                        results["efficient_frontier"],
                        x="Annualized Volatility",
                        y="Annualized Return"
                    )

                # =========================
                # REBALANCING TAB
                # =========================

                with tab_rebalancing:
                    st.header("Rebalancing Analysis")

                    st.subheader("Rebalancing Strategy Comparison")
                    st.dataframe(
                        results["rebalancing_summary"],
                        use_container_width=True
                    )

                    st.subheader("Final Value by Rebalancing Strategy")
                    rebalancing_chart = results["rebalancing_summary"][
                        ["Strategy", "Final Value"]
                    ].set_index("Strategy")
                    st.bar_chart(rebalancing_chart)

                    st.header("Transaction Cost Analysis")

                    st.dataframe(
                        results["transaction_cost_summary"],
                        use_container_width=True
                    )

                    st.subheader("Cost Drag by Strategy and Cost Assumption")
                    cost_drag_chart = results["transaction_cost_summary"][
                        ["Strategy", "Transaction Cost Rate", "Cost Drag"]
                    ].copy()

                    cost_drag_pivot = cost_drag_chart.pivot_table(
                        index="Strategy",
                        columns="Transaction Cost Rate",
                        values="Cost Drag"
                    )

                    st.bar_chart(cost_drag_pivot)

                # =========================
                # MARKET SENSITIVITY TAB
                # =========================

                with tab_market:
                    st.header("Market Sensitivity")

                    st.subheader("Benchmark Sensitivity")
                    st.dataframe(
                        results["market_sensitivity_summary"],
                        use_container_width=True
                    )

                    st.subheader("Upside / Downside Capture")
                    st.dataframe(
                        results["capture_summary"],
                        use_container_width=True
                    )

                    st.subheader("Rolling Beta")
                    st.line_chart(results["rolling_beta"])

                # =========================
                # DOWNLOADS TAB
                # =========================

                with tab_downloads:
                    st.header("Download Results")

                    st.download_button(
                        label="Download Performance Summary CSV",
                        data=convert_df_to_csv(performance_summary),
                        file_name="performance_summary.csv",
                        mime="text/csv"
                    )

                    st.download_button(
                        label="Download Monte Carlo Comparison CSV",
                        data=convert_df_to_csv(results["monte_carlo_comparison"]),
                        file_name="monte_carlo_comparison.csv",
                        mime="text/csv"
                    )

                    st.download_button(
                        label="Download Risk Parity Weights CSV",
                        data=convert_df_to_csv(risk_parity_df),
                        file_name="risk_parity_weights.csv",
                        mime="text/csv"
                    )

                    st.download_button(
                        label="Download Rebalancing Summary CSV",
                        data=convert_df_to_csv(results["rebalancing_summary"]),
                        file_name="rebalancing_summary.csv",
                        mime="text/csv"
                    )

                    st.download_button(
                        label="Download Transaction Cost Summary CSV",
                        data=convert_df_to_csv(results["transaction_cost_summary"]),
                        file_name="transaction_cost_summary.csv",
                        mime="text/csv"
                    )

                    st.download_button(
                        label="Download Market Sensitivity CSV",
                        data=convert_df_to_csv(results["market_sensitivity_summary"]),
                        file_name="market_sensitivity_summary.csv",
                        mime="text/csv"
                    )

            except ValueError as error:
                st.error("Input or data error.")
                st.warning(str(error))

            except KeyError as error:
                st.error("Ticker or benchmark data could not be found.")
                st.warning(
                    "Please check that all tickers and the benchmark are valid and available on Yahoo Finance."
                )
                st.exception(error)

            except Exception as error:
                st.error("An unexpected error occurred while running the analysis.")
                st.warning(
                    "Please check your tickers, weights, internet connection, and selected date range."
                )
                st.exception(error)