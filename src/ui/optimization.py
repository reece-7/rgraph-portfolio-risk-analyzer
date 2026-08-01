import pandas as pd
import streamlit as st


def render_optimization(
    results,
    risk_parity_df,
):
    """
    Renders portfolio optimization results.

    Includes:
    - Maximum Sharpe portfolio
    - Minimum Volatility portfolio
    - Risk Parity allocation
    - Efficient Frontier
    """

    st.header("Portfolio Optimization")

    st.subheader("Optimal Portfolios")

    st.dataframe(
        results["optimal_portfolios"],
        use_container_width=True,
    )

    st.subheader("Risk Parity Weights")

    st.dataframe(
        risk_parity_df,
        use_container_width=True,
    )

    st.subheader("Risk Parity Allocation")

    st.bar_chart(
        risk_parity_df[["Weight (%)"]]
    )

    st.subheader("Efficient Frontier")

    efficient_frontier = results["efficient_frontier"]

    st.scatter_chart(
        efficient_frontier,
        x="Annualized Volatility",
        y="Annualized Return",
    )

    with st.expander("View Efficient Frontier Data"):
        st.dataframe(
            efficient_frontier.head(100),
            use_container_width=True,
        )

        st.caption(
            "The table displays the first 100 simulated portfolios. "
            "The optimization uses the complete Efficient Frontier dataset."
        )