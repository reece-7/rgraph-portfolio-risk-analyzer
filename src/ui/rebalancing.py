import streamlit as st


def render_rebalancing(results):
    """
    Renders rebalancing strategy and transaction cost analysis.
    """

    rebalancing_summary = results["rebalancing_summary"]
    transaction_cost_summary = results["transaction_cost_summary"]

    # =========================
    # REBALANCING
    # =========================

    st.header("Rebalancing Analysis")

    st.subheader("Rebalancing Strategy Comparison")

    st.dataframe(
        rebalancing_summary,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Final Value by Rebalancing Strategy")

    rebalancing_chart = (
        rebalancing_summary[
            ["Strategy", "Final Value"]
        ]
        .set_index("Strategy")
    )

    st.bar_chart(rebalancing_chart)

    # =========================
    # TRANSACTION COSTS
    # =========================

    st.header("Transaction Cost Analysis")

    st.dataframe(
        transaction_cost_summary,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Cost Drag by Strategy and Cost Assumption")

    cost_drag_chart = transaction_cost_summary[
        [
            "Strategy",
            "Transaction Cost Rate",
            "Cost Drag",
        ]
    ].copy()

    cost_drag_pivot = cost_drag_chart.pivot_table(
        index="Strategy",
        columns="Transaction Cost Rate",
        values="Cost Drag",
    )

    st.bar_chart(cost_drag_pivot)

    with st.expander("How to interpret transaction cost drag"):
        st.write(
            """
            Cost drag measures the difference between the portfolio value
            obtained without transaction costs and the portfolio value obtained
            after applying the selected transaction cost assumption.

            More frequent rebalancing can keep the portfolio closer to its
            target allocation, but it can also generate higher turnover and
            therefore higher transaction costs.
            """
        )