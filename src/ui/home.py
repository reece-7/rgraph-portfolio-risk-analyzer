import streamlit as st


def render_home():
    """
    Renders the application title and introduction.
    """

    st.title("rGraph")
    st.subheader("Interactive Portfolio Risk Analyzer")

    st.write(
        """
        Analyze a custom portfolio using historical returns,
        Monte Carlo simulations,
        portfolio optimization,
        rebalancing analysis,
        transaction costs,
        and benchmark sensitivity.
        """
    )