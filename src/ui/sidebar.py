import pandas as pd
import streamlit as st


def render_section_header(
    number,
    title,
    description,
):
    """
    Renders a compact sidebar section heading.
    """

    st.html(
        f"""
        <div class="rg-sidebar-section">
            <div class="rg-sidebar-section-number">
                {number}
            </div>

            <div>
                <div class="rg-sidebar-section-title">
                    {title}
                </div>

                <div class="rg-sidebar-section-description">
                    {description}
                </div>
            </div>
        </div>
        """
    )


def render_sidebar():
    """
    Renders portfolio inputs and returns
    the selected configuration.
    """

    with st.sidebar:
        st.html(
            """
            <div class="rg-sidebar-header">
                <div class="rg-sidebar-wordmark">
                    <span>r</span>Graph
                </div>

                <div class="rg-sidebar-subtitle">
                    Portfolio configuration
                </div>
            </div>
            """
        )

        # =========================
        # PORTFOLIO
        # =========================

        render_section_header(
            number="01",
            title="Portfolio",
            description="Capital, history and benchmark",
        )

        initial_value = st.number_input(
            "Initial capital",
            min_value=100.0,
            value=10_000.0,
            step=1_000.0,
        )

        start_date = st.date_input(
            "Start date",
            value=pd.to_datetime("2018-01-01"),
        )

        benchmark_ticker = st.text_input(
            "Benchmark ticker",
            value="SPY",
        ).upper().strip()

        # =========================
        # SIMULATION
        # =========================

        render_section_header(
            number="02",
            title="Simulation",
            description="Monte Carlo configuration",
        )

        n_simulations = st.number_input(
            "Number of simulations",
            min_value=500,
            max_value=50_000,
            value=2_000,
            step=500,
        )

        fan_chart_lines = st.selectbox(
            "Fan chart detail",
            options=[1, 3, 5],
            index=2,
            help=(
                "Controls the number of percentile lines "
                "displayed in the fan chart."
            ),
        )

        time_horizon = st.number_input(
            "Forecast horizon",
            min_value=21,
            max_value=2520,
            value=252,
            step=21,
            help="Forecast horizon expressed in trading days.",
        )

        # =========================
        # ASSUMPTIONS
        # =========================

        render_section_header(
            number="03",
            title="Assumptions",
            description="Model and market conventions",
        )

        risk_free_rate_percent = st.number_input(
            "Risk-free rate (%)",
            min_value=0.0,
            max_value=20.0,
            value=0.0,
            step=0.25,
        )

        trading_days = st.selectbox(
            "Trading days per year",
            options=[252, 365],
            index=0,
            help=(
                "Use 252 for traditional financial assets "
                "and 365 for crypto-heavy portfolios."
            ),
        )

        # =========================
        # ASSETS
        # =========================

        render_section_header(
            number="04",
            title="Allocation",
            description="Assets and portfolio weights",
        )

        number_of_assets = st.number_input(
            "Number of assets",
            min_value=2,
            max_value=10,
            value=4,
            step=1,
        )

        st.html(
            """
            <div class="rg-assets-column-labels">
                <span></span>
                <span>Ticker</span>
                <span>Weight</span>
            </div>
            """
        )

        default_tickers = [
            "SPY",
            "QQQ",
            "TLT",
            "GLD",
        ]

        default_weights = [
            40.0,
            30.0,
            20.0,
            10.0,
        ]

        tickers = []
        weights_percent = []

        for index in range(int(number_of_assets)):
            default_ticker = (
                default_tickers[index]
                if index < len(default_tickers)
                else ""
            )

            default_weight = (
                default_weights[index]
                if index < len(default_weights)
                else 0.0
            )

            (
                number_column,
                ticker_column,
                weight_column,
            ) = st.columns(
                [0.22, 1.15, 0.85]
            )

            with number_column:
                st.html(
                    f"""
                    <div class="rg-sidebar-asset-number">
                        {index + 1:02d}
                    </div>
                    """
                )

            ticker = ticker_column.text_input(
                f"Asset {index + 1} ticker",
                value=default_ticker,
                key=f"ticker_{index}",
                placeholder="Ticker",
                label_visibility="collapsed",
            ).upper().strip()

            weight = weight_column.number_input(
                f"Asset {index + 1} weight",
                min_value=0.0,
                max_value=100.0,
                value=default_weight,
                step=1.0,
                key=f"weight_{index}",
                label_visibility="collapsed",
            )

            tickers.append(ticker)
            weights_percent.append(weight)

        total_weight_percent = sum(weights_percent)

        allocation_status_class = (
            "is-complete"
            if abs(total_weight_percent - 100.0) <= 0.01
            else "is-incomplete"
        )

        allocation_status_text = (
            "Allocation complete"
            if abs(total_weight_percent - 100.0) <= 0.01
            else "Allocation incomplete"
        )

        st.html(
            f"""
            <div class="rg-sidebar-summary">
                <div>
                    <span>Total allocation</span>
                    <strong>{total_weight_percent:.1f}%</strong>
                </div>

                <div class="
                    rg-sidebar-allocation-status
                    {allocation_status_class}
                ">
                    <span></span>
                    {allocation_status_text}
                </div>
            </div>
            """
        )

    return {
        "initial_value": float(initial_value),
        "start_date": start_date,
        "benchmark_ticker": benchmark_ticker,
        "n_simulations": int(n_simulations),
        "fan_chart_lines": int(fan_chart_lines),
        "time_horizon": int(time_horizon),
        "risk_free_rate": (
            float(risk_free_rate_percent) / 100
        ),
        "trading_days": int(trading_days),
        "tickers": tickers,
        "weights_percent": weights_percent,
    }