import numpy as np
import pandas as pd
import streamlit as st


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


def build_fan_chart(paths_df, fan_chart_lines):
    """
    Builds a Monte Carlo fan chart with selected percentile lines.
    """

    if fan_chart_lines == 1:
        return pd.DataFrame(
            {
                "Median": paths_df.quantile(
                    0.50,
                    axis=1,
                )
            }
        )

    if fan_chart_lines == 3:
        return pd.DataFrame(
            {
                "25th Percentile": paths_df.quantile(
                    0.25,
                    axis=1,
                ),
                "Median": paths_df.quantile(
                    0.50,
                    axis=1,
                ),
                "75th Percentile": paths_df.quantile(
                    0.75,
                    axis=1,
                ),
            }
        )

    return pd.DataFrame(
        {
            "5th Percentile": paths_df.quantile(
                0.05,
                axis=1,
            ),
            "25th Percentile": paths_df.quantile(
                0.25,
                axis=1,
            ),
            "Median": paths_df.quantile(
                0.50,
                axis=1,
            ),
            "75th Percentile": paths_df.quantile(
                0.75,
                axis=1,
            ),
            "95th Percentile": paths_df.quantile(
                0.95,
                axis=1,
            ),
        }
    )


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

    st.dataframe(
        results["monte_carlo_comparison"],
        use_container_width=True,
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

    st.dataframe(
        distribution_summary,
        use_container_width=True,
    )

    # =========================
    # PARAMETRIC FAN CHART
    # =========================

    render_chart_heading(
        eyebrow="PARAMETRIC MODEL",
        title="Parametric scenario paths",
        description=(
            f"{fan_chart_lines} percentile line(s) displayed "
            f"from {n_simulations:,} simulations."
        ),
    )

    parametric_fan_chart = build_fan_chart(
        parametric_paths_df,
        fan_chart_lines,
    )

    st.line_chart(
        parametric_fan_chart,
        use_container_width=True,
    )

    # =========================
    # BOOTSTRAP FAN CHART
    # =========================

    render_chart_heading(
        eyebrow="HISTORICAL BOOTSTRAP",
        title="Bootstrap scenario paths",
        description=(
            f"{fan_chart_lines} percentile line(s) displayed "
            f"from {n_simulations:,} simulations."
        ),
    )

    bootstrap_fan_chart = build_fan_chart(
        bootstrap_paths_df,
        fan_chart_lines,
    )

    st.line_chart(
        bootstrap_fan_chart,
        use_container_width=True,
    )

    # =========================
    # TERMINAL DISTRIBUTION
    # =========================

    render_chart_heading(
        eyebrow="OUTCOME DISTRIBUTION",
        title="Terminal value histogram",
        description=(
            "Percentage of scenarios falling inside each "
            "terminal portfolio-value interval."
        ),
    )

    histogram_df = build_distribution_histogram(
        parametric_values=parametric_values,
        bootstrap_values=bootstrap_values,
        bins=40,
    )

    st.bar_chart(
        histogram_df,
        use_container_width=True,
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