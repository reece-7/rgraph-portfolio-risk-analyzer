import pandas as pd
import streamlit as st


def convert_df_to_csv(dataframe):
    """
    Converts a DataFrame into UTF-8 encoded CSV data.
    """

    return dataframe.to_csv(
        index=True
    ).encode("utf-8")


def to_dataframe(data, column_name):
    """
    Converts a Series or array-like object
    into a DataFrame suitable for export.
    """

    if isinstance(data, pd.DataFrame):
        return data.copy()

    if isinstance(data, pd.Series):
        return data.to_frame(
            name=data.name or column_name
        )

    return pd.DataFrame(
        data,
        columns=[column_name],
    )


def render_download_category(
    number,
    title,
    description,
):
    """
    Renders a flat category heading.
    """

    st.html(
        f"""
        <div class="rg-download-category">
            <span class="rg-download-category-number">
                {number}
            </span>

            <div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>

            <div class="rg-download-category-line"></div>
        </div>
        """
    )


def render_download_row(
    title,
    description,
    dataframe,
    file_name,
    key,
):
    """
    Renders one export row and its CSV download action.
    """

    row_count = len(dataframe)
    column_count = len(dataframe.columns)

    with st.container(
        key=f"download_row_{key}"
    ):
        information_column, action_column = st.columns(
            [4, 1.15],
            vertical_alignment="center",
        )

        with information_column:
            st.html(
                f"""
                <div class="rg-download-row-copy">
                    <div class="rg-download-row-title">
                        {title}
                    </div>

                    <div class="rg-download-row-description">
                        {description}
                    </div>

                    <div class="rg-download-row-meta">
                        <span>{row_count:,} rows</span>
                        <span>{column_count:,} columns</span>
                        <span>CSV · UTF-8</span>
                    </div>
                </div>
                """
            )

        with action_column:
            st.download_button(
                label="Export CSV",
                data=convert_df_to_csv(dataframe),
                file_name=file_name,
                mime="text/csv",
                key=f"download_{key}",
                type="tertiary",
                icon=":material/download:",
                width="stretch",
            )


def render_downloads(results):
    """
    Renders all available CSV export options.
    """

    performance_summary = pd.DataFrame(
        [results["performance_summary"]],
        index=["Custom Portfolio"],
    )

    portfolio_values = to_dataframe(
        results["portfolio_values"],
        "Portfolio Value",
    )

    portfolio_returns = to_dataframe(
        results["portfolio_returns"],
        "Daily Return",
    )

    risk_parity_df = (
        results["risk_parity_weights"]
        .to_frame(name="Weight")
    )

    risk_parity_df["Weight (%)"] = (
        risk_parity_df["Weight"] * 100
    )

    monte_carlo_terminal_values = pd.DataFrame(
        {
            "Parametric Monte Carlo": (
                results["parametric_final_values"]
            ),
            "Bootstrap Monte Carlo": (
                results["bootstrap_final_values"]
            ),
        }
    )

    capture_summary = results[
        "capture_summary"
    ].copy()

    rolling_beta = results[
        "rolling_beta"
    ].copy()

    export_count = 13

    st.html(
        f"""
        <section class="rg-downloads">

            <div class="rg-section-heading">
                <div>
                    <span>ANALYSIS OUTPUT</span>
                    <h2>Downloads</h2>
                </div>

                <p>
                    Export the complete datasets generated during
                    the latest portfolio analysis.
                </p>
            </div>

            <div class="rg-download-summary">

                <div>
                    <span>Available datasets</span>
                    <strong>{export_count}</strong>
                </div>

                <div>
                    <span>File format</span>
                    <strong>CSV</strong>
                </div>

                <div>
                    <span>Encoding</span>
                    <strong>UTF-8</strong>
                </div>

                <div>
                    <span>Analysis state</span>
                    <strong class="positive">
                        Complete
                    </strong>
                </div>

            </div>

            <div class="rg-download-note">
                Every export reflects the latest completed analysis.
                Changing sidebar inputs does not alter these files until
                the portfolio is analyzed again.
            </div>

        </section>
        """
    )

    # =========================
    # PERFORMANCE
    # =========================

    render_download_category(
        number="01",
        title="Performance",
        description=(
            "Historical portfolio values, returns "
            "and summary metrics."
        ),
    )

    render_download_row(
        title="Performance summary",
        description=(
            "Return, volatility, Sharpe Ratio, drawdown, "
            "Value at Risk and Expected Shortfall."
        ),
        dataframe=performance_summary,
        file_name="performance_summary.csv",
        key="performance_summary",
    )

    render_download_row(
        title="Portfolio value history",
        description=(
            "Complete historical evolution of the "
            "portfolio's compounded value."
        ),
        dataframe=portfolio_values,
        file_name="portfolio_values.csv",
        key="portfolio_values",
    )

    render_download_row(
        title="Daily portfolio returns",
        description=(
            "Daily percentage returns used throughout "
            "the risk and performance calculations."
        ),
        dataframe=portfolio_returns,
        file_name="portfolio_returns.csv",
        key="portfolio_returns",
    )

    # =========================
    # SIMULATION
    # =========================

    render_download_category(
        number="02",
        title="Simulation",
        description=(
            "Monte Carlo risk statistics and "
            "simulated terminal outcomes."
        ),
    )

    render_download_row(
        title="Monte Carlo comparison",
        description=(
            "Comparison of risk metrics generated by "
            "parametric and bootstrap models."
        ),
        dataframe=results[
            "monte_carlo_comparison"
        ],
        file_name="monte_carlo_comparison.csv",
        key="monte_carlo_comparison",
    )

    render_download_row(
        title="Monte Carlo terminal values",
        description=(
            "Final portfolio value produced by every "
            "parametric and bootstrap simulation."
        ),
        dataframe=monte_carlo_terminal_values,
        file_name="monte_carlo_terminal_values.csv",
        key="monte_carlo_terminal_values",
    )

    # =========================
    # ALLOCATION
    # =========================

    render_download_category(
        number="03",
        title="Allocation",
        description=(
            "Optimized portfolios, Risk Parity "
            "and simulated risk-return allocations."
        ),
    )

    render_download_row(
        title="Optimal portfolios",
        description=(
            "Maximum-Sharpe and minimum-volatility "
            "portfolio allocations."
        ),
        dataframe=results[
            "optimal_portfolios"
        ],
        file_name="optimal_portfolios.csv",
        key="optimal_portfolios",
    )

    render_download_row(
        title="Risk Parity weights",
        description=(
            "Long-only allocation designed to balance "
            "risk contribution across assets."
        ),
        dataframe=risk_parity_df,
        file_name="risk_parity_weights.csv",
        key="risk_parity_weights",
    )

    render_download_row(
        title="Efficient Frontier dataset",
        description=(
            "Complete set of simulated portfolios with "
            "return, volatility, Sharpe Ratio and weights."
        ),
        dataframe=results[
            "efficient_frontier"
        ],
        file_name="efficient_frontier.csv",
        key="efficient_frontier",
    )

    # =========================
    # REBALANCING
    # =========================

    render_download_category(
        number="04",
        title="Rebalancing",
        description=(
            "Strategy comparison and transaction-cost "
            "sensitivity."
        ),
    )

    render_download_row(
        title="Rebalancing summary",
        description=(
            "Performance comparison across Buy & Hold, "
            "monthly, quarterly and annual rebalancing."
        ),
        dataframe=results[
            "rebalancing_summary"
        ],
        file_name="rebalancing_summary.csv",
        key="rebalancing_summary",
    )

    render_download_row(
        title="Transaction-cost summary",
        description=(
            "Performance, direct costs and cost drag "
            "under multiple transaction-cost assumptions."
        ),
        dataframe=results[
            "transaction_cost_summary"
        ],
        file_name="transaction_cost_summary.csv",
        key="transaction_cost_summary",
    )

    # =========================
    # MARKET
    # =========================

    render_download_category(
        number="05",
        title="Market relationship",
        description=(
            "Benchmark sensitivity, market participation "
            "and changing exposure."
        ),
    )

    render_download_row(
        title="Market sensitivity summary",
        description=(
            "Beta, correlation, active return, tracking "
            "error and Information Ratio."
        ),
        dataframe=results[
            "market_sensitivity_summary"
        ],
        file_name="market_sensitivity_summary.csv",
        key="market_sensitivity",
    )

    render_download_row(
        title="Capture analysis",
        description=(
            "Upside capture, downside capture and "
            "upside-to-downside capture ratio."
        ),
        dataframe=capture_summary,
        file_name="capture_summary.csv",
        key="capture_summary",
    )

    render_download_row(
        title="Rolling beta",
        description=(
            "Historical evolution of portfolio beta "
            "relative to the selected benchmark."
        ),
        dataframe=rolling_beta,
        file_name="rolling_beta.csv",
        key="rolling_beta",
    )