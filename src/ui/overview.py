import math

import streamlit as st

from src.ui.charts import (
    build_horizontal_allocation_chart,
)

def format_currency(value):
    """
    Formats a numeric value as currency.
    """

    return f"${value:,.0f}"


def format_percentage(value):
    """
    Formats a decimal value as a percentage.
    """

    return f"{value * 100:.2f}%"


def format_ratio(value):
    """
    Formats a ratio while handling missing values.
    """

    if value is None:
        return "—"

    try:
        if math.isnan(value):
            return "—"
    except TypeError:
        pass

    return f"{value:.2f}"


def render_metric_item(
    label,
    value,
    detail=None,
    tone="neutral",
):
    """
    Builds one metric in the flat overview strip.
    """

    detail_html = ""

    if detail:
        detail_html = f"""
        <span class="rg-overview-metric-detail">
            {detail}
        </span>
        """

    return f"""
    <div class="rg-overview-metric">
        <span class="rg-overview-metric-label">
            {label}
        </span>

        <strong class="rg-overview-metric-value {tone}">
            {value}
        </strong>

        {detail_html}
    </div>
    """


def render_overview(
    results,
    initial_value,
    setup_df,
):
    """
    Renders the portfolio overview dashboard.
    """

    performance = results["performance_summary"]

    final_value = performance["Final Value"]
    total_return = performance["Total Return"]
    annualized_return = performance["Annualized Return"]
    annualized_volatility = performance["Annualized Volatility"]
    sharpe_ratio = performance["Sharpe Ratio"]
    maximum_drawdown = performance["Maximum Drawdown"]
    historical_var = performance["Historical VaR 95%"]
    expected_shortfall = performance[
        "Historical Expected Shortfall 95%"
    ]

    return_tone = (
        "positive"
        if total_return >= 0
        else "negative"
    )

    sharpe_tone = (
        "positive"
        if sharpe_ratio >= 1
        else "neutral"
    )

    headline_metrics = "".join(
        [
            render_metric_item(
                label="Initial capital",
                value=format_currency(initial_value),
                detail="Starting portfolio value",
            ),
            render_metric_item(
                label="Final value",
                value=format_currency(final_value),
                detail="Latest historical value",
            ),
            render_metric_item(
                label="Total return",
                value=format_percentage(total_return),
                detail="Full analysis period",
                tone=return_tone,
            ),
            render_metric_item(
                label="Sharpe ratio",
                value=format_ratio(sharpe_ratio),
                detail="Risk-adjusted return",
                tone=sharpe_tone,
            ),
        ]
    )

    risk_metrics = "".join(
        [
            render_metric_item(
                label="Annualized return",
                value=format_percentage(annualized_return),
                tone=(
                    "positive"
                    if annualized_return >= 0
                    else "negative"
                ),
            ),
            render_metric_item(
                label="Annualized volatility",
                value=format_percentage(
                    annualized_volatility
                ),
            ),
            render_metric_item(
                label="Maximum drawdown",
                value=format_percentage(maximum_drawdown),
                tone="negative",
            ),
            render_metric_item(
                label="Daily VaR 95%",
                value=format_percentage(historical_var),
                tone="negative",
            ),
            render_metric_item(
                label="Expected shortfall 95%",
                value=format_percentage(expected_shortfall),
                tone="negative",
            ),
        ]
    )

    st.html(
        f"""
        <section class="rg-overview">

            <div class="rg-section-heading">
                <div>
                    <span>PORTFOLIO SNAPSHOT</span>
                    <h2>Overview</h2>
                </div>

                <p>
                    Historical performance and risk profile of the
                    latest completed analysis.
                </p>
            </div>

            <div class="rg-overview-primary-metrics">
                {headline_metrics}
            </div>

            <div class="rg-overview-risk-heading">
                <span>RISK PROFILE</span>

                <div></div>
            </div>

            <div class="rg-overview-risk-metrics">
                {risk_metrics}
            </div>

        </section>
        """
    )

    st.subheader("Portfolio Allocation")

    allocation_df = (
        setup_df[["Ticker", "Weight (%)"]]
        .set_index("Ticker")
    )

    allocation_chart = (
        build_horizontal_allocation_chart(
            allocation_data=allocation_df,
            value_column="Weight (%)",
        )
    )

    st.altair_chart(
        allocation_chart,
        use_container_width=True,
    )

    st.subheader("Portfolio Value Over Time")

    st.line_chart(
        results["portfolio_values"],
        use_container_width=True,
    )