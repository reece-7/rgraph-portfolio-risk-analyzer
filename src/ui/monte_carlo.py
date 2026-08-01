from html import escape

import numpy as np
import pandas as pd
import streamlit as st

from src.ui.charts import (
    build_monte_carlo_fan_chart,
    build_terminal_distribution_chart,
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

def format_table_currency(value):
    """
    Formats currency values for compact financial tables.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"${value:,.0f}"


def format_table_percentage(value):
    """
    Formats decimal values as percentages.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"{value * 100:.2f}%"


def format_monte_carlo_metric(column, value):
    """
    Formats the Monte Carlo comparison table
    according to the type of metric.
    """

    if column in {
        "Mean Final Value",
        "Median Final Value",
    }:
        return format_table_currency(value)

    if column in {
        "Probability of Loss",
        "95% Value at Risk",
        "95% Expected Shortfall",
    }:
        return format_table_percentage(value)

    if value is None or pd.isna(value):
        return "—"

    if isinstance(value, (int, float, np.number)):
        return f"{value:,.2f}"

    return str(value)


def format_distribution_statistic(column, value):
    """
    Formats descriptive distribution statistics.
    """

    if value is None or pd.isna(value):
        return "—"

    if column == "count":
        return f"{int(value):,}"

    return format_table_currency(value)


def get_monte_carlo_cell_tone(column, value):
    """
    Returns a visual tone for selected risk values.
    """

    if value is None or pd.isna(value):
        return ""

    if column in {
        "95% Value at Risk",
        "95% Expected Shortfall",
    }:
        return "is-negative"

    if column == "Probability of Loss":
        if value >= 0.25:
            return "is-negative"

        if value >= 0.10:
            return "is-warning"

        return "is-positive"

    return ""


def build_financial_table_html(
    dataframe,
    index_title,
    value_formatter,
    tone_resolver=None,
    compact=False,
):
    """
    Converts a DataFrame into a styled HTML financial table.
    """

    table_class = "rg-mc-table"

    if compact:
        table_class += " is-compact"

    html_parts = [
        '<div class="rg-mc-table-scroll">',
        f'<table class="{table_class}">',
        "<thead>",
        "<tr>",
        f"<th>{escape(str(index_title))}</th>",
    ]

    for column in dataframe.columns:
        html_parts.append(
            f"<th>{escape(str(column))}</th>"
        )

    html_parts.extend(
        [
            "</tr>",
            "</thead>",
            "<tbody>",
        ]
    )

    for index, row in dataframe.iterrows():
        html_parts.append("<tr>")

        html_parts.append(
            f"""
            <th scope="row">
                {escape(str(index))}
            </th>
            """
        )

        for column in dataframe.columns:
            value = row[column]

            formatted_value = value_formatter(
                column,
                value,
            )

            tone_class = ""

            if tone_resolver is not None:
                tone_class = tone_resolver(
                    column,
                    value,
                )

            html_parts.append(
                f"""
                <td class="{tone_class}">
                    {escape(str(formatted_value))}
                </td>
                """
            )

        html_parts.append("</tr>")

    html_parts.extend(
        [
            "</tbody>",
            "</table>",
            "</div>",
        ]
    )

    return "".join(html_parts)

def build_distribution_histogram(
    parametric_values,
    bootstrap_values,
    bins=40,
):
    """
    Groups final simulated values into common histogram bins.

    Values are represented as a percentage of simulations
    so the two models remain directly comparable.
    """

    combined_values = np.concatenate(
        [
            parametric_values,
            bootstrap_values,
        ]
    )

    minimum_value = combined_values.min()
    maximum_value = combined_values.max()

    if minimum_value == maximum_value:
        maximum_value = minimum_value + 1

    bin_edges = np.linspace(
        minimum_value,
        maximum_value,
        bins + 1,
    )

    parametric_counts, _ = np.histogram(
        parametric_values,
        bins=bin_edges,
    )

    bootstrap_counts, _ = np.histogram(
        bootstrap_values,
        bins=bin_edges,
    )

    bin_centers = (
        bin_edges[:-1] + bin_edges[1:]
    ) / 2

    histogram_df = pd.DataFrame(
        {
            "Parametric (%)": (
                parametric_counts
                / len(parametric_values)
                * 100
            ),
            "Bootstrap (%)": (
                bootstrap_counts
                / len(bootstrap_values)
                * 100
            ),
        },
        index=bin_centers,
    )

    histogram_df.index.name = "Final Portfolio Value"

    return histogram_df


def render_simulation_metric(
    label,
    value,
    detail,
    tone="neutral",
):
    """
    Builds one simulation metric.
    """

    return f"""
    <div class="rg-simulation-metric">
        <span class="rg-simulation-metric-label">
            {label}
        </span>

        <strong class="rg-simulation-metric-value {tone}">
            {value}
        </strong>

        <span class="rg-simulation-metric-detail">
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


def build_simulation_reading(
    parametric_loss_probability,
    bootstrap_loss_probability,
    parametric_fifth_percentile,
    bootstrap_fifth_percentile,
):
    """
    Creates a concise interpretation of both simulation models.
    """

    if (
        bootstrap_loss_probability
        > parametric_loss_probability
    ):
        downside_model = "bootstrap"
        probability_difference = (
            bootstrap_loss_probability
            - parametric_loss_probability
        )

    else:
        downside_model = "parametric"
        probability_difference = (
            parametric_loss_probability
            - bootstrap_loss_probability
        )

    if (
        bootstrap_fifth_percentile
        < parametric_fifth_percentile
    ):
        tail_model = "bootstrap"
    else:
        tail_model = "parametric"

    return (
        f"The {downside_model} model produces the higher probability "
        f"of finishing below the initial capital, with a difference of "
        f"{probability_difference * 100:.2f} percentage points. "
        f"The {tail_model} model also generates the more conservative "
        f"5th-percentile terminal value."
    )


def render_monte_carlo(
    results,
    fan_chart_lines,
    n_simulations,
    initial_value,
):
    """
    Renders Monte Carlo metrics, summaries,
    fan charts and terminal distributions.
    """

    parametric_values = np.asarray(
        results["parametric_final_values"],
        dtype=float,
    )

    bootstrap_values = np.asarray(
        results["bootstrap_final_values"],
        dtype=float,
    )

    monte_carlo_final_values = pd.DataFrame(
        {
            "Parametric Monte Carlo": parametric_values,
            "Bootstrap Monte Carlo": bootstrap_values,
        }
    )

    # The engine returns:
    # simulations x trading days.
    #
    # The transpose produces:
    # trading days x simulations.
    parametric_paths_df = pd.DataFrame(
        results["parametric_paths"]
    ).T

    bootstrap_paths_df = pd.DataFrame(
        results["bootstrap_paths"]
    ).T

    simulation_start_date = results.get(
        "simulation_start_date"
    )

    simulation_end_date = results.get(
        "simulation_end_date"
    )

    resolved_time_horizon = results.get(
        "time_horizon",
        len(parametric_paths_df),
    )

    parametric_median = np.median(
        parametric_values
    )

    bootstrap_median = np.median(
        bootstrap_values
    )

    parametric_loss_probability = np.mean(
        parametric_values < initial_value
    )

    bootstrap_loss_probability = np.mean(
        bootstrap_values < initial_value
    )

    parametric_fifth_percentile = np.percentile(
        parametric_values,
        5,
    )

    bootstrap_fifth_percentile = np.percentile(
        bootstrap_values,
        5,
    )

    if (
        simulation_start_date is not None
        and simulation_end_date is not None
    ):
        formatted_start_date = pd.Timestamp(
            simulation_start_date
        ).strftime("%d %b %Y")

        formatted_end_date = pd.Timestamp(
            simulation_end_date
        ).strftime("%d %b %Y")

        st.html(
            f"""
            <div class="rg-analysis-state is-current">
                <span class="rg-analysis-state-dot"></span>

                <strong>Forecast window</strong>

                <span>
                    {formatted_start_date}
                    →
                    {formatted_end_date}
                    ·
                    {resolved_time_horizon:,}
                    simulated periods
                </span>
            </div>
            """
        )

    else:
        st.html(
            f"""
            <div class="rg-analysis-state is-current">
                <span class="rg-analysis-state-dot"></span>

                <strong>Forecast horizon</strong>

                <span>
                    {resolved_time_horizon:,}
                    simulated periods from the final
                    historical market observation.
                </span>
            </div>
            """
        )

    metric_strip = "".join(
        [
            render_simulation_metric(
                label="Parametric median",
                value=format_currency(
                    parametric_median
                ),
                detail="Median terminal value",
                tone=(
                    "positive"
                    if parametric_median >= initial_value
                    else "negative"
                ),
            ),
            render_simulation_metric(
                label="Bootstrap median",
                value=format_currency(
                    bootstrap_median
                ),
                detail="Median terminal value",
                tone=(
                    "positive"
                    if bootstrap_median >= initial_value
                    else "negative"
                ),
            ),
            render_simulation_metric(
                label="Parametric loss risk",
                value=format_percentage(
                    parametric_loss_probability
                ),
                detail="Probability below initial capital",
                tone=(
                    "negative"
                    if parametric_loss_probability >= 0.25
                    else "neutral"
                ),
            ),
            render_simulation_metric(
                label="Bootstrap loss risk",
                value=format_percentage(
                    bootstrap_loss_probability
                ),
                detail="Probability below initial capital",
                tone=(
                    "negative"
                    if bootstrap_loss_probability >= 0.25
                    else "neutral"
                ),
            ),
        ]
    )

    simulation_reading = build_simulation_reading(
        parametric_loss_probability=(
            parametric_loss_probability
        ),
        bootstrap_loss_probability=(
            bootstrap_loss_probability
        ),
        parametric_fifth_percentile=(
            parametric_fifth_percentile
        ),
        bootstrap_fifth_percentile=(
            bootstrap_fifth_percentile
        ),
    )

    st.html(
        f"""
        <section class="rg-simulation">

            <div class="rg-section-heading">
                <div>
                    <span>FORWARD-LOOKING RISK</span>
                    <h2>Monte Carlo simulation</h2>
                </div>

                <p>
                    Comparison of parametric and historical bootstrap
                    scenarios across {n_simulations:,} simulated paths.
                </p>
            </div>

            <div class="rg-simulation-strip">
                {metric_strip}
            </div>

            <div class="rg-simulation-reading">
                <span>MODEL COMPARISON</span>

                <p>
                    {simulation_reading}
                </p>
            </div>

        </section>
        """
    )

    # =========================
    # RISK METRICS
    # =========================

    render_chart_heading(
        eyebrow="MODEL OUTPUT",
        title="Monte Carlo risk metrics",
        description=(
            "Downside and terminal-value statistics "
            "calculated by both simulation engines."
        ),
    )

    monte_carlo_comparison = (
        results["monte_carlo_comparison"]
        .copy()
    )

    monte_carlo_table_html = (
        build_financial_table_html(
            dataframe=monte_carlo_comparison,
            index_title="Simulation model",
            value_formatter=format_monte_carlo_metric,
            tone_resolver=get_monte_carlo_cell_tone,
            compact=True,
        )
    )

    st.html(
        monte_carlo_table_html
    )

    # =========================
    # DISTRIBUTION SUMMARY
    # =========================

    render_chart_heading(
        eyebrow="TERMINAL STATISTICS",
        title="Final value summary",
        description=(
            "Descriptive statistics for all simulated "
            "terminal portfolio values."
        ),
    )

    distribution_summary = (
        monte_carlo_final_values.describe(
            percentiles=[
                0.05,
                0.25,
                0.50,
                0.75,
                0.95,
            ]
        )
    )

    distribution_summary_for_display = (
        distribution_summary.T
    )

    distribution_table_html = (
        build_financial_table_html(
            dataframe=distribution_summary_for_display,
            index_title="Simulation model",
            value_formatter=format_distribution_statistic,
            compact=True,
        )
    )

    st.html(
        distribution_table_html
    )
    # =========================
    # PARAMETRIC FAN CHART
    # =========================

    render_chart_heading(
        eyebrow="PARAMETRIC MODEL",
        title="Parametric scenario range",
        description=(
            f"Median path and percentile uncertainty bands "
            f"derived from {n_simulations:,} simulations."
        ),
    )

    parametric_fan_chart = (
        build_monte_carlo_fan_chart(
            paths_df=parametric_paths_df,
            fan_chart_lines=fan_chart_lines,
            initial_value=initial_value,
            model_name="Parametric",
            accent_color="#35C7FF",
        )
    )

    st.altair_chart(
        parametric_fan_chart,
        width="stretch",
        theme=None,
    )

    # =========================
    # BOOTSTRAP FAN CHART
    # =========================

    render_chart_heading(
        eyebrow="HISTORICAL BOOTSTRAP",
        title="Bootstrap scenario range",
        description=(
            f"Median path and percentile uncertainty bands "
            f"derived from {n_simulations:,} resampled scenarios."
        ),
    )

    bootstrap_fan_chart = (
        build_monte_carlo_fan_chart(
            paths_df=bootstrap_paths_df,
            fan_chart_lines=fan_chart_lines,
            initial_value=initial_value,
            model_name="Bootstrap",
            accent_color="#68DDB2",
        )
    )

    st.altair_chart(
        bootstrap_fan_chart,
        width="stretch",
        theme=None,
    )

    # =========================
    # TERMINAL DISTRIBUTION
    # =========================

    render_chart_heading(
        eyebrow="OUTCOME DISTRIBUTION",
        title="Terminal value distribution",
        description=(
            "Comparison of simulated terminal outcomes, "
            "including initial capital and model medians."
        ),
    )

    terminal_distribution_chart = (
        build_terminal_distribution_chart(
            parametric_values=parametric_values,
            bootstrap_values=bootstrap_values,
            initial_value=initial_value,
            bins=45,
        )
    )

    st.altair_chart(
        terminal_distribution_chart,
        width="stretch",
        theme=None,
    )

    with st.expander(
        "How to interpret Monte Carlo simulation"
    ):
        st.write(
            """
            The median represents the middle simulated outcome:
            half of the scenarios finish above it and half below it.

            Loss probability measures how often the simulated terminal
            portfolio value finishes below the original capital.

            The 5th percentile is a downside-tail estimate. Only around
            5% of simulated outcomes finish below that value.

            Parametric simulation assumes returns follow an estimated
            statistical process. Bootstrap simulation instead resamples
            observed historical returns and therefore preserves more of
            the historical return behaviour.
            """
        )