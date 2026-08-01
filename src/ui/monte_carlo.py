import pandas as pd
import streamlit as st


def build_fan_chart(paths_df, fan_chart_lines):
    """
    Builds a Monte Carlo fan chart with selected percentile lines.
    """

    if fan_chart_lines == 1:
        return pd.DataFrame({
            "Median": paths_df.quantile(0.50, axis=1)
        })

    if fan_chart_lines == 3:
        return pd.DataFrame({
            "25th Percentile": paths_df.quantile(0.25, axis=1),
            "Median": paths_df.quantile(0.50, axis=1),
            "75th Percentile": paths_df.quantile(0.75, axis=1),
        })

    return pd.DataFrame({
        "5th Percentile": paths_df.quantile(0.05, axis=1),
        "25th Percentile": paths_df.quantile(0.25, axis=1),
        "Median": paths_df.quantile(0.50, axis=1),
        "75th Percentile": paths_df.quantile(0.75, axis=1),
        "95th Percentile": paths_df.quantile(0.95, axis=1),
    })


def render_monte_carlo(
    results,
    fan_chart_lines,
    n_simulations,
):
    """
    Renders Monte Carlo metrics, summaries, and fan charts.
    """

    monte_carlo_final_values = pd.DataFrame({
        "Parametric Monte Carlo": results["parametric_final_values"],
        "Bootstrap Monte Carlo": results["bootstrap_final_values"],
    })

    parametric_paths_df = pd.DataFrame(
        results["parametric_paths"]
    ).T

    bootstrap_paths_df = pd.DataFrame(
        results["bootstrap_paths"]
    ).T

    st.header("Monte Carlo Simulation")

    st.subheader("Monte Carlo Risk Metrics")
    st.dataframe(
        results["monte_carlo_comparison"],
        use_container_width=True,
    )

    st.subheader("Final Value Distribution Summary")
    st.dataframe(
        monte_carlo_final_values.describe(),
        use_container_width=True,
    )

    st.subheader("Parametric Monte Carlo Fan Chart")

    parametric_fan_chart = build_fan_chart(
        parametric_paths_df,
        fan_chart_lines,
    )

    st.line_chart(parametric_fan_chart)

    st.caption(
        f"The chart displays {fan_chart_lines} percentile line(s). "
        f"The analysis uses {n_simulations:,} total simulations."
    )

    st.subheader("Bootstrap Monte Carlo Fan Chart")

    bootstrap_fan_chart = build_fan_chart(
        bootstrap_paths_df,
        fan_chart_lines,
    )

    st.line_chart(bootstrap_fan_chart)

    st.caption(
        f"The chart displays {fan_chart_lines} percentile line(s). "
        f"The analysis uses {n_simulations:,} total simulations."
    )

    st.subheader("Monte Carlo Final Value Distribution")
    st.bar_chart(
        monte_carlo_final_values,
    )