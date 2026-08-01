import pandas as pd
import streamlit as st


def render_performance(results):
    """
    Renders historical portfolio performance,
    portfolio value, and daily returns.
    """

    performance_summary = pd.DataFrame(
        [results["performance_summary"]],
        index=["Custom Portfolio"],
    )

    st.header("Performance Summary")

    st.dataframe(
        performance_summary,
        use_container_width=True,
    )

    st.subheader("Portfolio Value Over Time")

    st.line_chart(
        results["portfolio_values"],
    )

    st.subheader("Daily Portfolio Returns")

    st.line_chart(
        results["portfolio_returns"],
    )

    with st.expander("How to interpret these results"):
        st.write(
            """
            Portfolio value shows how the initial investment evolved
            during the selected historical period.

            Daily portfolio returns represent the percentage change
            in portfolio value from one trading day to the next.

            The performance summary combines return and risk metrics
            to provide an overall assessment of the portfolio.
            """
        )