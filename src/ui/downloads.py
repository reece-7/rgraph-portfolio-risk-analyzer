import pandas as pd
import streamlit as st


def convert_df_to_csv(dataframe):
    """
    Converts a DataFrame into UTF-8 encoded CSV data.
    """

    return dataframe.to_csv(index=True).encode("utf-8")


def render_downloads(results):
    """
    Renders all CSV download options.
    """

    performance_summary = pd.DataFrame(
        [results["performance_summary"]],
        index=["Custom Portfolio"],
    )

    risk_parity_df = results["risk_parity_weights"].to_frame(
        name="Weight"
    )

    risk_parity_df["Weight (%)"] = (
        risk_parity_df["Weight"] * 100
    )

    st.header("Download Results")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download Performance Summary CSV",
            data=convert_df_to_csv(performance_summary),
            file_name="performance_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.download_button(
            label="Download Risk Parity Weights CSV",
            data=convert_df_to_csv(risk_parity_df),
            file_name="risk_parity_weights.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.download_button(
            label="Download Transaction Cost Summary CSV",
            data=convert_df_to_csv(
                results["transaction_cost_summary"]
            ),
            file_name="transaction_cost_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="Download Monte Carlo Comparison CSV",
            data=convert_df_to_csv(
                results["monte_carlo_comparison"]
            ),
            file_name="monte_carlo_comparison.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.download_button(
            label="Download Rebalancing Summary CSV",
            data=convert_df_to_csv(
                results["rebalancing_summary"]
            ),
            file_name="rebalancing_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.download_button(
            label="Download Market Sensitivity CSV",
            data=convert_df_to_csv(
                results["market_sensitivity_summary"]
            ),
            file_name="market_sensitivity_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.caption(
        "CSV files contain the complete results generated "
        "during the latest portfolio analysis."
    )