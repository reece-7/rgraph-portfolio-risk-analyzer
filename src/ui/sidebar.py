import pandas as pd
import streamlit as st


def render_sidebar():
    """
    Renders portfolio inputs and returns the selected configuration.
    """

    st.sidebar.header("Portfolio Inputs")

    initial_value = st.sidebar.number_input(
        "Initial capital",
        min_value=100.0,
        value=10_000.0,
        step=1_000.0
    )

    start_date = st.sidebar.date_input(
        "Start date",
        value=pd.to_datetime("2018-01-01")
    )

    benchmark_ticker = st.sidebar.text_input(
        "Benchmark ticker",
        value="SPY"
    ).upper().strip()

    n_simulations = st.sidebar.number_input(
        "Number of Monte Carlo simulations",
        min_value=500,
        max_value=50_000,
        value=2_000,
        step=500
    )

    fan_chart_lines = st.sidebar.selectbox(
        "Monte Carlo fan chart detail",
        options=[1, 3, 5],
        index=2,
        help="Choose how many percentile lines to display."
    )

    time_horizon = st.sidebar.number_input(
        "Monte Carlo horizon in trading days",
        min_value=21,
        max_value=2520,
        value=252,
        step=21
    )

    risk_free_rate_percent = st.sidebar.number_input(
        "Risk-free rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=0.0,
        step=0.25
    )

    trading_days = st.sidebar.selectbox(
        "Trading days assumption",
        options=[252, 365],
        index=0,
        help="Use 252 for stocks/ETFs and 365 for crypto-heavy portfolios."
    )

    st.sidebar.header("Assets")

    number_of_assets = st.sidebar.number_input(
        "How many assets are in your portfolio?",
        min_value=2,
        max_value=10,
        value=4,
        step=1
    )

    default_tickers = ["SPY", "QQQ", "TLT", "GLD"]
    default_weights = [40.0, 30.0, 20.0, 10.0]

    tickers = []
    weights_percent = []

    for i in range(int(number_of_assets)):
        default_ticker = default_tickers[i] if i < len(default_tickers) else ""
        default_weight = default_weights[i] if i < len(default_weights) else 0.0

        ticker_col, weight_col = st.sidebar.columns(2)

        ticker = ticker_col.text_input(
            f"Asset {i + 1} ticker",
            value=default_ticker,
            key=f"ticker_{i}"
        ).upper().strip()

        weight = weight_col.number_input(
            f"Weight {i + 1} (%)",
            min_value=0.0,
            max_value=100.0,
            value=default_weight,
            step=1.0,
            key=f"weight_{i}"
        )

        tickers.append(ticker)
        weights_percent.append(weight)

    return {
        "initial_value": float(initial_value),
        "start_date": start_date,
        "benchmark_ticker": benchmark_ticker,
        "n_simulations": int(n_simulations),
        "fan_chart_lines": int(fan_chart_lines),
        "time_horizon": int(time_horizon),
        "risk_free_rate": float(risk_free_rate_percent) / 100,
        "trading_days": int(trading_days),
        "tickers": tickers,
        "weights_percent": weights_percent,
    }