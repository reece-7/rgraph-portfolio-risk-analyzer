import pandas as pd
import streamlit as st

from html import escape
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

def build_analysis_signature(inputs):
    """
    Builds a stable representation of analysis inputs
    for detecting changes after an analysis.
    """

    normalized_weights = tuple(
        sorted(
            (
                str(ticker).upper().strip(),
                round(float(weight), 10),
            )
            for ticker, weight in inputs["weights"].items()
        )
    )

    return (
        tuple(
            str(ticker).upper().strip()
            for ticker in inputs["tickers"]
        ),
        normalized_weights,
        round(float(inputs["initial_value"]), 2),
        str(inputs["start_date"]),
        str(inputs.get("end_date") or ""),
        str(inputs.get("forecast_mode") or ""),
        str(inputs.get("simulation_end_date") or ""),
        str(
            inputs["benchmark_ticker"]
        ).upper().strip(),
        int(inputs["n_simulations"]),
        int(inputs["time_horizon"]),
        int(inputs["trading_days"]),
        round(
            float(inputs["risk_free_rate"]),
            10,
        ),
    )

@st.cache_data(
    ttl=3600,
    max_entries=3,
    show_spinner=False,
)
def get_cached_analysis(
    tickers,
    weights_items,
    start_date,
    end_date,
    initial_value,
    n_simulations,
    time_horizon,
    simulation_end_date,
    trading_days,
    risk_free_rate,
    benchmark_ticker,
    _progress_callback=None,
):
    weights = dict(weights_items)

    return analyze_portfolio(
        tickers=list(tickers),
        weights=weights,
        start_date=start_date,
        end_date=end_date,
        initial_value=initial_value,
        n_simulations=n_simulations,
        time_horizon=time_horizon,
        simulation_end_date=simulation_end_date,
        trading_days=trading_days,
        risk_free_rate=risk_free_rate,
        benchmark_ticker=benchmark_ticker,
        transaction_cost_rates={
            "0.00%": 0.0000,
            "0.05%": 0.0005,
            "0.10%": 0.0010,
            "0.25%": 0.0025,
        },
        progress_callback=_progress_callback,
    )


render_home()

sidebar_inputs = render_sidebar()
initial_value = sidebar_inputs["initial_value"]
start_date = sidebar_inputs["start_date"]
end_date = sidebar_inputs["end_date"]
benchmark_ticker = sidebar_inputs[
    "benchmark_ticker"
]
n_simulations = sidebar_inputs[
    "n_simulations"
]
fan_chart_lines = sidebar_inputs[
    "fan_chart_lines"
]
forecast_mode = sidebar_inputs[
    "forecast_mode"
]
simulation_end_date = sidebar_inputs[
    "simulation_end_date"
]
time_horizon = sidebar_inputs[
    "time_horizon"
]
risk_free_rate = sidebar_inputs[
    "risk_free_rate"
]
trading_days = sidebar_inputs[
    "trading_days"
]
tickers = sidebar_inputs["tickers"]
weights_percent = sidebar_inputs[
    "weights_percent"
]

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

current_analysis_inputs = {
    "tickers": list(valid_tickers),
    "weights": dict(weights),
    "initial_value": float(initial_value),
    "start_date": str(start_date),
    "end_date": (
        str(end_date)
        if end_date is not None
        else None
    ),
    "forecast_mode": forecast_mode,
    "simulation_end_date": (
        str(simulation_end_date)
        if simulation_end_date is not None
        else None
    ),
    "benchmark_ticker": benchmark_ticker,
    "n_simulations": int(n_simulations),
    "time_horizon": int(time_horizon),
    "trading_days": int(trading_days),
    "risk_free_rate": float(risk_free_rate),
}

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
        analysis_status = st.status(
            "Preparing portfolio analysis",
            state="running",
            expanded=False,
        )

        def update_analysis_status(label):
            analysis_status.update(
                label=label,
                state="running",
                expanded=False,
            )
        def show_analysis_error(
            label,
            message,
        ):
            """
            Shows a closed error status followed by
            one flat explanatory line.
            """

            analysis_status.update(
                label=label,
                state="error",
                expanded=False,
            )

            st.html(
                f"""
                <div class="rg-analysis-error-line">
                    <span></span>

                    <p>
                        {escape(str(message))}
                    </p>
                </div>
                """
            )

        try:
            results = get_cached_analysis(
                tickers=tuple(valid_tickers),
                weights_items=tuple(
                    sorted(weights.items())
                ),
                start_date=str(start_date),
                end_date=(
                    str(end_date)
                    if end_date is not None
                    else None
                ),
                initial_value=float(initial_value),
                n_simulations=int(n_simulations),
                time_horizon=int(time_horizon),
                simulation_end_date=(
                    str(simulation_end_date)
                    if simulation_end_date is not None
                    else None
                ),
                trading_days=int(trading_days),
                risk_free_rate=float(risk_free_rate),
                benchmark_ticker=benchmark_ticker,
                _progress_callback=(
                    update_analysis_status
                ),
            )

            st.session_state.analysis_results = results

            st.session_state.analysis_inputs = {
                **current_analysis_inputs,
                "tickers": list(
                    current_analysis_inputs["tickers"]
                ),
                "weights": dict(
                    current_analysis_inputs["weights"]
                ),
            }

            analysis_status.update(
                label="Portfolio analysis complete",
                state="complete",
                expanded=False,
            )

            st.html(
                """
                <div class="rg-analysis-complete">
                    <span class="rg-analysis-complete-dot"></span>

                    <strong>Analysis complete</strong>

                    <span>
                        Dashboard updated using the latest allocation.
                    </span>
                </div>
                """
            )

        except ValueError as error:
            show_analysis_error(
                label="Analysis stopped",
                message=str(error),
            )

        except KeyError as error:
            missing_item = (
                str(error)
                .strip("'")
                .strip('"')
            )

            show_analysis_error(
                label="Market data unavailable",
                message=(
                    "A required ticker or data field "
                    f"could not be found: {missing_item}."
                ),
            )

        except Exception as error:
            show_analysis_error(
                label="Portfolio analysis failed",
                message=(
                    "An unexpected error occurred while "
                    f"running the analysis: {error}"
                ),
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

inputs_have_changed = (
    build_analysis_signature(
        current_analysis_inputs
    )
    != build_analysis_signature(
        analysis_inputs
    )
)

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


if inputs_have_changed:
    st.html(
        """
        <div class="rg-analysis-state is-stale">
            <span class="rg-analysis-state-dot"></span>

            <strong>Inputs changed</strong>

            <span>
                Dashboard results still refer to the previous analysis.
                Run the analysis again to synchronize them.
            </span>
        </div>
        """
    )

else:
    st.html(
        """
        <div class="rg-analysis-state is-current">
            <span class="rg-analysis-state-dot"></span>

            <strong>Results synchronized</strong>

            <span>
                Dashboard results match the current portfolio inputs.
            </span>
        </div>
        """
    )

# =========================
# DASHBOARD NAVIGATION
# =========================

st.html(
    """
    <div class="rg-dashboard-navigation-header">
        <div>
            <span>ANALYSIS WORKSPACE</span>
            <h2>Portfolio dashboard</h2>
        </div>

        <p>
            Explore the latest completed portfolio analysis.
        </p>
    </div>
    """
)

dashboard_section = st.segmented_control(
    "Dashboard section",
    options=[
        "Overview",
        "Performance",
        "Simulation",
        "Allocation",
        "Rebalancing",
        "Market",
        "Downloads",
    ],
    default="Overview",
    key="dashboard_navigation",
    label_visibility="collapsed",
    width="stretch",
)


# =========================
# CONDITIONAL RENDERING
# =========================

if dashboard_section == "Overview":
    render_overview(
        results=results,
        initial_value=analyzed_initial_value,
        setup_df=analyzed_setup_df,
    )

elif dashboard_section == "Performance":
    render_performance(
        results=results,
    )

elif dashboard_section == "Simulation":
    render_monte_carlo(
        results=results,
        fan_chart_lines=fan_chart_lines,
        n_simulations=analyzed_n_simulations,
        initial_value=analyzed_initial_value,
    )

elif dashboard_section == "Allocation":
    render_optimization(
        results=results,
        risk_parity_df=risk_parity_df,
        current_weights=analyzed_weights,
    )

elif dashboard_section == "Rebalancing":
    render_rebalancing(
        results=results,
    )

elif dashboard_section == "Market":
    render_market(
        results=results,
        benchmark_ticker=analyzed_benchmark_ticker,
    )

elif dashboard_section == "Downloads":
    render_downloads(
        results=results,
    )

