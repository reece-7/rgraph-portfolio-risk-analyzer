import pandas as pd
import streamlit as st

from src.ui.charts import (
    build_daily_returns_chart,
    build_drawdown_chart,
    build_performance_value_chart,
)

from src.ui.tables import (
    render_financial_table,
)

def to_series(data, name):
    """
    Converts a Series or one-column DataFrame
    into a clean pandas Series.
    """

    if isinstance(data, pd.DataFrame):
        if data.shape[1] != 1:
            raise ValueError(
                f"{name} must contain exactly one column."
            )

        series = data.iloc[:, 0].copy()

    else:
        series = pd.Series(data).copy()

    series = series.dropna()
    series.name = name

    return series


def format_percentage(value):
    """
    Formats a decimal value as a percentage.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"{value * 100:.2f}%"


def render_performance_metric(
    label,
    value,
    detail,
    tone="neutral",
):
    """
    Builds one item in the performance metric strip.
    """

    return f"""
    <div class="rg-performance-metric">
        <span class="rg-performance-metric-label">
            {label}
        </span>

        <strong class="rg-performance-metric-value {tone}">
            {value}
        </strong>

        <span class="rg-performance-metric-detail">
            {detail}
        </span>
    </div>
    """


def render_chart_heading(
    eyebrow,
    title,
    description,
):
    """
    Renders a consistent heading above a chart.
    """

    st.html(
        f"""
        <div class="rg-chart-heading">
            <div>
                <span>{eyebrow}</span>
                <h3>{title}</h3>
            </div>

            <p>{description}</p>
        </div>
        """
    )


def build_performance_reading(
    sharpe_ratio,
    maximum_drawdown,
):
    """
    Creates a concise interpretation of risk-adjusted
    performance and historical downside.
    """

    if sharpe_ratio >= 1:
        sharpe_text = (
            "Risk-adjusted performance was historically strong."
        )

    elif sharpe_ratio >= 0.5:
        sharpe_text = (
            "Risk-adjusted performance was historically moderate."
        )

    else:
        sharpe_text = (
            "Historical returns provided limited compensation "
            "for the volatility experienced."
        )

    if maximum_drawdown <= -0.30:
        drawdown_text = (
            "The portfolio also experienced a material historical drawdown."
        )

    elif maximum_drawdown <= -0.15:
        drawdown_text = (
            "Historical downside was meaningful but not extreme."
        )

    else:
        drawdown_text = (
            "Historical peak-to-trough losses remained relatively contained."
        )

    return f"{sharpe_text} {drawdown_text}"


def render_performance(results):
    """
    Renders historical performance, portfolio value,
    daily returns, and drawdown analysis.
    """

    performance = results["performance_summary"]

    portfolio_values = to_series(
        results["portfolio_values"],
        "Portfolio Value",
    )

    portfolio_returns = to_series(
        results["portfolio_returns"],
        "Daily Return",
    )

    drawdowns = (
        portfolio_values
        / portfolio_values.cummax()
        - 1
    )

    drawdowns.name = "Drawdown"

    best_day = portfolio_returns.max()
    worst_day = portfolio_returns.min()

    positive_day_ratio = (
        portfolio_returns.gt(0).mean()
    )

    current_drawdown = drawdowns.iloc[-1]

    sharpe_ratio = performance["Sharpe Ratio"]
    maximum_drawdown = performance["Maximum Drawdown"]

    metric_strip = "".join(
        [
            render_performance_metric(
                label="Best day",
                value=format_percentage(best_day),
                detail="Highest daily return",
                tone="positive",
            ),
            render_performance_metric(
                label="Worst day",
                value=format_percentage(worst_day),
                detail="Lowest daily return",
                tone="negative",
            ),
            render_performance_metric(
                label="Positive days",
                value=format_percentage(
                    positive_day_ratio
                ),
                detail="Share of profitable sessions",
            ),
            render_performance_metric(
                label="Current drawdown",
                value=format_percentage(
                    current_drawdown
                ),
                detail="Distance from latest peak",
                tone=(
                    "negative"
                    if current_drawdown < 0
                    else "positive"
                ),
            ),
        ]
    )

    performance_reading = build_performance_reading(
        sharpe_ratio=sharpe_ratio,
        maximum_drawdown=maximum_drawdown,
    )

    st.html(
        f"""
        <section class="rg-performance">

            <div class="rg-section-heading">
                <div>
                    <span>HISTORICAL ANALYSIS</span>
                    <h2>Performance</h2>
                </div>

                <p>
                    Growth, daily variation and downside behaviour
                    across the selected historical period.
                </p>
            </div>

            <div class="rg-performance-strip">
                {metric_strip}
            </div>

            <div class="rg-performance-reading">
                <span>PERFORMANCE READING</span>

                <p>
                    {performance_reading}
                </p>
            </div>

        </section>
        """
    )

    # =========================
    # COMPLETE SUMMARY
    # =========================

    render_chart_heading(
        eyebrow="COMPLETE DATASET",
        title="Performance summary",
        description=(
            "Complete return and risk metrics generated "
            "by the analytics engine."
        ),
    )

    performance_summary = pd.DataFrame(
        [performance],
        index=["Custom Portfolio"],
    )

    render_financial_table(
        performance_summary,
        index_label="Portfolio",
        percent_columns=[
            "Total Return",
            "Annualized Return",
            "Annualized Volatility",
            "Maximum Drawdown",
            "Historical VaR 95%",
            "Historical Expected Shortfall 95%",
        ],
        currency_columns=[
            "Initial Value",
            "Final Value",
        ],
        ratio_columns=[
            "Sharpe Ratio",
        ],
        key="performance_summary_table",
    )

    # =========================
    # PORTFOLIO VALUE
    # =========================

    render_chart_heading(
        eyebrow="WEALTH PATH",
        title="Portfolio value over time",
        description=(
            "Historical evolution of the original "
            "capital after daily compounding."
        ),
    )

    portfolio_value_chart = (
        build_performance_value_chart(
            portfolio_values
        )
    )

    st.altair_chart(
        portfolio_value_chart,
        width="stretch",
        theme=None,
    )

    # =========================
    # DRAWDOWN
    # =========================

    render_chart_heading(
        eyebrow="DOWNSIDE",
        title="Drawdown from historical peak",
        description=(
            "Percentage decline from the previous "
            "highest portfolio value."
        ),
    )

    drawdown_chart = (
        build_drawdown_chart(
            drawdowns
        )
    )

    st.altair_chart(
        drawdown_chart,
        width="stretch",
        theme=None,
    )

    # =========================
    # DAILY RETURNS
    # =========================

    render_chart_heading(
        eyebrow="DAILY VARIATION",
        title="Daily portfolio returns",
        description=(
            "Day-to-day percentage changes in "
            "the historical portfolio value."
        ),
    )

    daily_returns_chart = (
        build_daily_returns_chart(
            portfolio_returns
        )
    )

    st.altair_chart(
        daily_returns_chart,
        width="stretch",
        theme=None,
    )

    with st.expander("How to interpret performance analysis"):
        st.write(
            """
            Portfolio value shows how the initial investment evolved
            over the selected historical period.

            Drawdown measures the percentage decline from the
            portfolio's previous historical peak. A drawdown of -20%
            means the portfolio was worth 20% less than its prior peak.

            Daily returns show short-term variability. Large positive
            and negative observations indicate periods of elevated
            market volatility.
            """
        )