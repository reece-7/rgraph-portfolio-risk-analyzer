import pandas as pd
import streamlit as st


def render_overview(
    results,
    initial_value,
    setup_df,
):
    """
    Renders the portfolio overview dashboard.
    """

    performance = results["performance_summary"]

    st.header("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Initial Capital",
        f"{initial_value:,.2f}",
    )

    col2.metric(
        "Final Value",
        f"{performance['Final Value']:,.2f}",
    )

    col3.metric(
        "Total Return",
        f"{performance['Total Return'] * 100:.2f}%",
    )

    col4.metric(
        "Sharpe Ratio",
        f"{performance['Sharpe Ratio']:.2f}",
    )

    st.subheader("Portfolio Allocation")

    allocation_df = (
        setup_df[["Ticker", "Weight (%)"]]
        .set_index("Ticker")
    )

    st.bar_chart(allocation_df)

    st.subheader("Portfolio Value Over Time")
    st.line_chart(results["portfolio_values"])