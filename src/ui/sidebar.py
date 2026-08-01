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

        historical_end_mode = st.selectbox(
            "Historical end",
            options=[
                "Latest available",
                "Custom date",
            ],
            index=0,
            help=(
                "Latest available uses the most recent market data. "
                "Custom date allows an analysis as of a past date."
            ),
        )

        if historical_end_mode == "Custom date":
            end_date = st.date_input(
                "Historical end date",
                value=pd.Timestamp.today().date(),
                min_value=start_date,
                max_value=pd.Timestamp.today().date(),
            )

        else:
            end_date = None
            
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

        forecast_mode = st.segmented_control(
            "Forecast horizon mode",
            options=[
                "Target date",
                "Trading days",
            ],
            default="Target date",
            width="stretch",
        )

        forecast_anchor = pd.Timestamp(
            end_date
            if end_date is not None
            else pd.Timestamp.today().date()
        ).normalize()

        if forecast_mode == "Target date":
            default_simulation_end = (
                forecast_anchor
                + pd.DateOffset(years=1)
            ).date()

            simulation_end_date = st.date_input(
                "Simulation end date",
                value=default_simulation_end,
                min_value=(
                    forecast_anchor
                    + pd.Timedelta(days=21)
                ).date(),
                help=(
                    "The Monte Carlo scenarios will extend "
                    "approximately to this future date."
                ),
            )

            # Temporary value. The engine recalculates the
            # exact horizon from the selected target date.
            time_horizon = 252

            forecast_calendar_days = (
                pd.Timestamp(simulation_end_date)
                - forecast_anchor
            ).days

            if forecast_calendar_days > 1095:
                st.caption(
                    "Long-horizon scenario: uncertainty and "
                    "model sensitivity increase materially "
                    "beyond three years."
                )

        else:
            simulation_end_date = None

            time_horizon = st.number_input(
                "Forecast horizon",
                min_value=21,
                max_value=2520,
                value=252,
                step=21,
                help=(
                    "Forecast horizon expressed in "
                    "simulated periods."
                ),
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
        "end_date": end_date,
        "benchmark_ticker": benchmark_ticker,
        "n_simulations": int(n_simulations),
        "fan_chart_lines": int(fan_chart_lines),
        "forecast_mode": forecast_mode,
        "simulation_end_date": simulation_end_date,
        "time_horizon": int(time_horizon),
        "risk_free_rate": (
            float(risk_free_rate_percent) / 100
        ),
        "trading_days": int(trading_days),
        "tickers": tickers,
        "weights_percent": weights_percent,
    }