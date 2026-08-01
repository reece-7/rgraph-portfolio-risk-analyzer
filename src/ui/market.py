import streamlit as st


def render_market(
    results,
    benchmark_ticker,
):
    """
    Renders benchmark sensitivity, capture ratios,
    and rolling beta analysis.
    """

    st.header("Market Sensitivity")

    # =========================
    # BENCHMARK SENSITIVITY
    # =========================

    st.subheader("Benchmark Sensitivity")

    st.dataframe(
        results["market_sensitivity_summary"],
        use_container_width=True,
    )

    st.caption(
        f"Portfolio sensitivity metrics are calculated relative "
        f"to the selected benchmark: {benchmark_ticker}."
    )

    # =========================
    # CAPTURE RATIOS
    # =========================

    st.subheader("Upside / Downside Capture")

    st.dataframe(
        results["capture_summary"],
        use_container_width=True,
    )

    with st.expander("How to interpret capture ratios"):
        st.write(
            """
            Upside capture measures how much of the benchmark's positive
            performance the portfolio captured during rising market periods.

            Downside capture measures how much of the benchmark's negative
            performance the portfolio experienced during falling market periods.

            Generally, a portfolio aims to achieve strong upside capture while
            keeping downside capture relatively low.
            """
        )

    # =========================
    # ROLLING BETA
    # =========================

    st.subheader("Rolling Beta")

    st.line_chart(
        results["rolling_beta"],
    )

    st.caption(
        f"Rolling beta shows how the portfolio's sensitivity to "
        f"{benchmark_ticker} changes through time."
    )