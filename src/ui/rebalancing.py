import pandas as pd
import streamlit as st

from src.ui.charts import (
    build_rebalancing_heatmap,
    build_strategy_lollipop_chart,
)

def format_currency(value):
    """
    Formats a numeric value as currency.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"${value:,.0f}"


def format_percentage(value):
    """
    Formats a decimal value as a percentage.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"{value * 100:.2f}%"


def format_ratio(value):
    """
    Formats a numeric ratio.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"{value:.2f}"


def render_rebalancing_metric(
    label,
    value,
    detail,
    tone="neutral",
):
    """
    Builds one rebalancing metric.
    """

    return f"""
    <div class="rg-rebalancing-metric">
        <span class="rg-rebalancing-metric-label">
            {label}
        </span>

        <strong class="rg-rebalancing-metric-value {tone}">
            {value}
        </strong>

        <span class="rg-rebalancing-metric-detail">
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
    Renders a consistent heading above a chart or table.
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


def parse_cost_rate(cost_rate):
    """
    Converts a percentage label such as '0.25%'
    into a numeric value.
    """

    try:
        return float(
            str(cost_rate).replace("%", "").strip()
        )
    except (TypeError, ValueError):
        return 0.0


def build_rebalancing_reading(
    best_final_strategy,
    best_final_value,
    buy_hold_value,
    best_sharpe_strategy,
    highest_cost_rate,
    highest_drag_strategy,
    highest_cost_drag,
):
    """
    Creates a concise interpretation of the
    rebalancing and transaction-cost results.
    """

    value_difference = (
        best_final_value - buy_hold_value
    )

    if best_final_strategy == "Buy & Hold":
        value_text = (
            "Buy & Hold generated the highest final value "
            "over the historical period."
        )

    elif value_difference > 0:
        value_text = (
            f"{best_final_strategy} generated the highest final value, "
            f"finishing {format_currency(value_difference)} above "
            f"Buy & Hold."
        )

    else:
        value_text = (
            f"{best_final_strategy} produced the strongest final value, "
            "although its advantage over Buy & Hold was limited."
        )

    sharpe_text = (
        f"{best_sharpe_strategy} delivered the highest "
        "historical Sharpe Ratio."
    )

    cost_text = (
        f"Under the highest modeled transaction-cost assumption "
        f"({highest_cost_rate}), {highest_drag_strategy} experienced "
        f"the largest cost drag at "
        f"{format_currency(highest_cost_drag)}."
    )

    return f"{value_text} {sharpe_text} {cost_text}"


def render_rebalancing(results):
    """
    Renders rebalancing strategy performance
    and transaction-cost analysis.
    """

    rebalancing_summary = (
        results["rebalancing_summary"].copy()
    )

    transaction_cost_summary = (
        results["transaction_cost_summary"].copy()
    )

    rebalancing_paths = results.get(
        "rebalancing_paths",
        {},
    )

    # =========================
    # IDENTIFY REFERENCE STRATEGIES
    # =========================

    best_final_row = rebalancing_summary.loc[
        rebalancing_summary["Final Value"].idxmax()
    ]

    best_sharpe_row = rebalancing_summary.loc[
        rebalancing_summary["Sharpe Ratio"].idxmax()
    ]

    lowest_drawdown_row = rebalancing_summary.loc[
        rebalancing_summary[
            "Maximum Drawdown"
        ].idxmax()
    ]

    best_final_strategy = best_final_row["Strategy"]
    best_final_value = best_final_row["Final Value"]

    best_sharpe_strategy = best_sharpe_row["Strategy"]
    best_sharpe_ratio = best_sharpe_row["Sharpe Ratio"]

    lowest_drawdown_strategy = (
        lowest_drawdown_row["Strategy"]
    )

    lowest_drawdown_value = (
        lowest_drawdown_row["Maximum Drawdown"]
    )

    buy_hold_rows = rebalancing_summary[
        rebalancing_summary["Strategy"]
        == "Buy & Hold"
    ]

    if not buy_hold_rows.empty:
        buy_hold_value = (
            buy_hold_rows.iloc[0]["Final Value"]
        )
    else:
        buy_hold_value = best_final_value

    # =========================
    # TRANSACTION COST REFERENCES
    # =========================

    cost_rates = (
        transaction_cost_summary[
            "Transaction Cost Rate"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    highest_cost_rate = max(
        cost_rates,
        key=parse_cost_rate,
    )

    highest_cost_rows = transaction_cost_summary[
        transaction_cost_summary[
            "Transaction Cost Rate"
        ]
        == highest_cost_rate
    ]

    highest_drag_row = highest_cost_rows.loc[
        highest_cost_rows["Cost Drag"].idxmax()
    ]

    highest_drag_strategy = (
        highest_drag_row["Strategy"]
    )

    highest_cost_drag = (
        highest_drag_row["Cost Drag"]
    )

    # =========================
    # METRIC STRIP
    # =========================

    metric_strip = "".join(
        [
            render_rebalancing_metric(
                label="Best final value",
                value=format_currency(
                    best_final_value
                ),
                detail=best_final_strategy,
                tone="positive",
            ),
            render_rebalancing_metric(
                label="Best Sharpe Ratio",
                value=format_ratio(
                    best_sharpe_ratio
                ),
                detail=best_sharpe_strategy,
                tone="positive",
            ),
            render_rebalancing_metric(
                label="Lowest drawdown",
                value=format_percentage(
                    lowest_drawdown_value
                ),
                detail=lowest_drawdown_strategy,
            ),
            render_rebalancing_metric(
                label="Maximum cost drag",
                value=format_currency(
                    highest_cost_drag
                ),
                detail=(
                    f"{highest_drag_strategy} "
                    f"at {highest_cost_rate}"
                ),
                tone="negative",
            ),
        ]
    )

    rebalancing_reading = build_rebalancing_reading(
        best_final_strategy=best_final_strategy,
        best_final_value=best_final_value,
        buy_hold_value=buy_hold_value,
        best_sharpe_strategy=best_sharpe_strategy,
        highest_cost_rate=highest_cost_rate,
        highest_drag_strategy=highest_drag_strategy,
        highest_cost_drag=highest_cost_drag,
    )

    st.html(
        f"""
        <section class="rg-rebalancing">

            <div class="rg-section-heading">
                <div>
                    <span>PORTFOLIO MAINTENANCE</span>
                    <h2>Rebalancing</h2>
                </div>

                <p>
                    Compare Buy & Hold with monthly, quarterly
                    and annual portfolio rebalancing.
                </p>
            </div>

            <div class="rg-rebalancing-strip">
                {metric_strip}
            </div>

            <div class="rg-rebalancing-reading">
                <span>STRATEGY READING</span>

                <p>
                    {rebalancing_reading}
                </p>
            </div>

        </section>
        """
    )

    # =========================
    # STRATEGY PATHS
    # =========================

    render_chart_heading(
        eyebrow="HISTORICAL PATHS",
        title="Portfolio value by rebalancing strategy",
        description=(
            "Historical growth of the portfolio under each "
            "rebalancing frequency."
        ),
    )

    custom_portfolio_paths = rebalancing_paths.get(
        "Custom Portfolio",
        {},
    )

    if custom_portfolio_paths:
        strategy_paths_df = pd.DataFrame(
            custom_portfolio_paths
        )

        st.line_chart(
            strategy_paths_df,
            use_container_width=True,
        )

    else:
        st.caption(
            "Historical strategy paths are not available."
        )

    # =========================
    # STRATEGY SUMMARY
    # =========================

    render_chart_heading(
        eyebrow="STRATEGY METRICS",
        title="Rebalancing strategy comparison",
        description=(
            "Return, volatility, Sharpe Ratio and downside "
            "statistics for every rebalancing policy."
        ),
    )

    formatted_rebalancing_summary = (
        rebalancing_summary.copy()
    )

    percentage_columns = [
        "Total Return",
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown",
    ]

    currency_columns = [
        "Final Value",
        "Total Transaction Costs",
    ]

    for column in percentage_columns:
        if column in formatted_rebalancing_summary.columns:
            formatted_rebalancing_summary[column] = (
                formatted_rebalancing_summary[column]
                .map(format_percentage)
            )

    for column in currency_columns:
        if column in formatted_rebalancing_summary.columns:
            formatted_rebalancing_summary[column] = (
                formatted_rebalancing_summary[column]
                .map(format_currency)
            )

    if (
        "Sharpe Ratio"
        in formatted_rebalancing_summary.columns
    ):
        formatted_rebalancing_summary[
            "Sharpe Ratio"
        ] = (
            formatted_rebalancing_summary[
                "Sharpe Ratio"
            ]
            .map(format_ratio)
        )

    st.dataframe(
        formatted_rebalancing_summary,
        use_container_width=True,
        hide_index=True,
    )

    # =========================
    # FINAL VALUE CHART
    # =========================

    render_chart_heading(
        eyebrow="TERMINAL COMPARISON",
        title="Final value by strategy",
        description=(
            "Final historical portfolio value produced by "
            "each rebalancing frequency."
        ),
    )

    final_value_chart = (
        build_strategy_lollipop_chart(
            rebalancing_summary
        )
    )

    st.altair_chart(
        final_value_chart,
        width="stretch",
        theme=None,
    )

    # =========================
    # TRANSACTION COST TABLE
    # =========================

    render_chart_heading(
        eyebrow="IMPLEMENTATION COSTS",
        title="Transaction-cost analysis",
        description=(
            "Performance after applying multiple cost rates "
            "to trades generated by each strategy."
        ),
    )

    formatted_transaction_summary = (
        transaction_cost_summary.copy()
    )

    transaction_percentage_columns = [
        "Total Return",
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown",
    ]

    transaction_currency_columns = [
        "Final Value",
        "Total Transaction Costs",
        "Zero Cost Final Value",
        "Cost Drag",
    ]

    for column in transaction_percentage_columns:
        if column in formatted_transaction_summary.columns:
            formatted_transaction_summary[column] = (
                formatted_transaction_summary[column]
                .map(format_percentage)
            )

    for column in transaction_currency_columns:
        if column in formatted_transaction_summary.columns:
            formatted_transaction_summary[column] = (
                formatted_transaction_summary[column]
                .map(format_currency)
            )

    if (
        "Sharpe Ratio"
        in formatted_transaction_summary.columns
    ):
        formatted_transaction_summary[
            "Sharpe Ratio"
        ] = (
            formatted_transaction_summary[
                "Sharpe Ratio"
            ]
            .map(format_ratio)
        )

    st.dataframe(
        formatted_transaction_summary,
        use_container_width=True,
        hide_index=True,
    )

    # =========================
    # COST DRAG
    # =========================

    render_chart_heading(
        eyebrow="COST SENSITIVITY",
        title="Cost drag by strategy",
        description=(
            "Difference between each zero-cost result and "
            "its corresponding after-cost portfolio value."
        ),
    )

    cost_drag_heatmap = (
        build_rebalancing_heatmap(
            transaction_cost_summary=(
                transaction_cost_summary
            ),
            value_column="Cost Drag",
            value_title="Cost drag",
        )
    )

    st.altair_chart(
        cost_drag_heatmap,
        width="stretch",
        theme=None,
    )

    # =========================
    # TOTAL COSTS
    # =========================

    render_chart_heading(
        eyebrow="DIRECT COSTS",
        title="Total transaction costs",
        description=(
            "Cumulative dollar amount paid under each "
            "strategy and transaction-cost assumption."
        ),
    )

    total_cost_heatmap = (
        build_rebalancing_heatmap(
            transaction_cost_summary=(
                transaction_cost_summary
            ),
            value_column="Total Transaction Costs",
            value_title="Transaction costs",
        )
    )

    st.altair_chart(
        total_cost_heatmap,
        width="stretch",
        theme=None,
    )

    with st.expander(
        "How to interpret rebalancing and transaction costs"
    ):
        st.write(
            """
            Rebalancing restores the portfolio to its target
            allocation after market movements cause asset weights
            to drift.

            More frequent rebalancing can keep the portfolio closer
            to its intended risk profile, but it also creates more
            trades and potentially higher transaction costs.

            Cost drag measures the difference between the portfolio's
            zero-cost final value and its final value after applying
            transaction costs.

            The strategy with the highest return is not necessarily
            the strategy with the highest Sharpe Ratio or the lowest
            drawdown. Each metric evaluates a different aspect of
            portfolio performance.
            """
        )