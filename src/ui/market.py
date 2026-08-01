import pandas as pd
import streamlit as st


def format_percentage(value):
    """
    Formats a decimal value as a percentage.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"{value * 100:.2f}%"


def format_ratio(value):
    """
    Formats a numeric ratio.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"{value:.2f}"


def render_market_metric(
    label,
    value,
    detail,
    tone="neutral",
):
    """
    Builds one market-sensitivity metric.
    """

    return f"""
    <div class="rg-market-metric">
        <span class="rg-market-metric-label">
            {label}
        </span>

        <strong class="rg-market-metric-value {tone}">
            {value}
        </strong>

        <span class="rg-market-metric-detail">
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


def build_market_reading(
    beta,
    correlation,
    active_return,
    capture_ratio,
    benchmark_ticker,
):
    """
    Creates an automatic interpretation of
    benchmark sensitivity.
    """

    if beta >= 1.10:
        beta_text = (
            f"The portfolio has historically been more sensitive "
            f"than {benchmark_ticker} to market movements."
        )

    elif beta <= 0.90:
        beta_text = (
            f"The portfolio has historically behaved more defensively "
            f"than {benchmark_ticker}."
        )

    else:
        beta_text = (
            f"The portfolio has historically shown sensitivity "
            f"similar to {benchmark_ticker}."
        )

    if correlation >= 0.80:
        correlation_text = (
            "Its return pattern has been strongly aligned "
            "with the benchmark."
        )

    elif correlation >= 0.50:
        correlation_text = (
            "Its return pattern has shown a moderate relationship "
            "with the benchmark."
        )

    else:
        correlation_text = (
            "Its historical relationship with the benchmark "
            "has been relatively limited."
        )

    if active_return > 0:
        active_text = (
            "The portfolio generated a positive annualized "
            "active return."
        )

    elif active_return < 0:
        active_text = (
            "The portfolio generated a negative annualized "
            "active return."
        )

    else:
        active_text = (
            "The portfolio generated little historical "
            "active return."
        )

    if pd.isna(capture_ratio):
        capture_text = (
            "The capture relationship could not be evaluated reliably."
        )

    elif capture_ratio > 1:
        capture_text = (
            "Its upside-to-downside capture relationship "
            "was historically favourable."
        )

    else:
        capture_text = (
            "Its upside-to-downside capture relationship "
            "was historically unfavourable."
        )

    return (
        f"{beta_text} {correlation_text} "
        f"{active_text} {capture_text}"
    )


def render_market(
    results,
    benchmark_ticker,
):
    """
    Renders benchmark comparison, sensitivity,
    capture ratios and rolling beta.
    """

    market_summary = (
        results["market_sensitivity_summary"].copy()
    )

    capture_summary = (
        results["capture_summary"].copy()
    )

    rolling_beta = results["rolling_beta"].copy()

    market_row = market_summary.iloc[0]
    capture_row = capture_summary.iloc[0]

    beta = market_row["Beta vs Benchmark"]

    correlation = market_row[
        "Correlation vs Benchmark"
    ]

    active_return = market_row[
        "Annualized Active Return"
    ]

    tracking_error = market_row[
        "Tracking Error"
    ]

    information_ratio = market_row[
        "Information Ratio"
    ]

    upside_capture = capture_row[
        "Upside Capture"
    ]

    downside_capture = capture_row[
        "Downside Capture"
    ]

    capture_ratio = capture_row[
        "Capture Ratio"
    ]

    valid_rolling_beta = rolling_beta.dropna()

    if not valid_rolling_beta.empty:
        current_rolling_beta = (
            valid_rolling_beta.iloc[-1, 0]
        )
    else:
        current_rolling_beta = beta

    metric_strip = "".join(
        [
            render_market_metric(
                label="Beta",
                value=format_ratio(beta),
                detail=f"Sensitivity vs {benchmark_ticker}",
            ),
            render_market_metric(
                label="Correlation",
                value=format_ratio(correlation),
                detail="Return relationship",
            ),
            render_market_metric(
                label="Active return",
                value=format_percentage(active_return),
                detail="Annualized vs benchmark",
                tone=(
                    "positive"
                    if active_return >= 0
                    else "negative"
                ),
            ),
            render_market_metric(
                label="Tracking error",
                value=format_percentage(tracking_error),
                detail="Active-return volatility",
            ),
            render_market_metric(
                label="Information ratio",
                value=format_ratio(information_ratio),
                detail="Active return per unit of risk",
                tone=(
                    "positive"
                    if information_ratio > 0
                    else "negative"
                ),
            ),
        ]
    )

    capture_metrics = "".join(
        [
            render_market_metric(
                label="Upside capture",
                value=format_percentage(upside_capture),
                detail="Participation during positive benchmark days",
                tone=(
                    "positive"
                    if upside_capture >= 1
                    else "neutral"
                ),
            ),
            render_market_metric(
                label="Downside capture",
                value=format_percentage(downside_capture),
                detail="Participation during negative benchmark days",
                tone=(
                    "positive"
                    if downside_capture < 1
                    else "negative"
                ),
            ),
            render_market_metric(
                label="Capture ratio",
                value=format_ratio(capture_ratio),
                detail="Upside capture divided by downside capture",
                tone=(
                    "positive"
                    if capture_ratio > 1
                    else "negative"
                ),
            ),
            render_market_metric(
                label="Latest rolling beta",
                value=format_ratio(current_rolling_beta),
                detail="Most recent rolling estimate",
            ),
        ]
    )

    market_reading = build_market_reading(
        beta=beta,
        correlation=correlation,
        active_return=active_return,
        capture_ratio=capture_ratio,
        benchmark_ticker=benchmark_ticker,
    )

    st.html(
        f"""
        <section class="rg-market">

            <div class="rg-section-heading">
                <div>
                    <span>BENCHMARK RELATIONSHIP</span>
                    <h2>Market sensitivity</h2>
                </div>

                <p>
                    Historical exposure and relative performance
                    compared with {benchmark_ticker}.
                </p>
            </div>

            <div class="rg-market-strip">
                {metric_strip}
            </div>

            <div class="rg-market-reading">
                <span>MARKET READING</span>

                <p>
                    {market_reading}
                </p>
            </div>

        </section>
        """
    )

    # =========================
    # RELATIVE GROWTH
    # =========================

    render_chart_heading(
        eyebrow="RELATIVE PERFORMANCE",
        title=f"Portfolio vs {benchmark_ticker}",
        description=(
            "Growth of 100 invested in the portfolio and "
            "the selected benchmark over the same period."
        ),
    )

    all_returns = results["returns"]

    if benchmark_ticker in all_returns.columns:
        benchmark_returns = all_returns[
            benchmark_ticker
        ]

        portfolio_returns = results[
            "portfolio_returns"
        ]

        comparison_returns = pd.concat(
            [
                portfolio_returns.rename(
                    "Portfolio"
                ),
                benchmark_returns.rename(
                    benchmark_ticker
                ),
            ],
            axis=1,
        ).dropna()

        normalized_growth = (
            1 + comparison_returns
        ).cumprod() * 100

        st.line_chart(
            normalized_growth,
            use_container_width=True,
        )

    else:
        st.caption(
            "Benchmark return history is not available."
        )

    # =========================
    # MARKET SUMMARY
    # =========================

    render_chart_heading(
        eyebrow="RELATIVE RISK",
        title="Benchmark sensitivity summary",
        description=(
            "Beta, correlation and active-risk metrics "
            "relative to the selected benchmark."
        ),
    )

    formatted_market_summary = (
        market_summary.copy()
    )

    for column in [
        "Annualized Active Return",
        "Tracking Error",
    ]:
        if column in formatted_market_summary.columns:
            formatted_market_summary[column] = (
                formatted_market_summary[column]
                .map(format_percentage)
            )

    for column in [
        "Beta vs Benchmark",
        "Correlation vs Benchmark",
        "Information Ratio",
    ]:
        if column in formatted_market_summary.columns:
            formatted_market_summary[column] = (
                formatted_market_summary[column]
                .map(format_ratio)
            )

    st.dataframe(
        formatted_market_summary,
        use_container_width=True,
    )

    # =========================
    # CAPTURE ANALYSIS
    # =========================

    render_chart_heading(
        eyebrow="MARKET PARTICIPATION",
        title="Upside and downside capture",
        description=(
            "Portfolio participation during positive "
            "and negative benchmark sessions."
        ),
    )

    st.html(
        f"""
        <div class="rg-market-capture-strip">
            {capture_metrics}
        </div>
        """
    )

    formatted_capture_summary = (
        capture_summary.copy()
    )

    for column in [
        "Upside Capture",
        "Downside Capture",
    ]:
        if column in formatted_capture_summary.columns:
            formatted_capture_summary[column] = (
                formatted_capture_summary[column]
                .map(format_percentage)
            )

    if "Capture Ratio" in formatted_capture_summary.columns:
        formatted_capture_summary[
            "Capture Ratio"
        ] = (
            formatted_capture_summary[
                "Capture Ratio"
            ]
            .map(format_ratio)
        )

    st.dataframe(
        formatted_capture_summary,
        use_container_width=True,
    )

    # =========================
    # ROLLING BETA
    # =========================

    render_chart_heading(
        eyebrow="CHANGING EXPOSURE",
        title="Rolling beta",
        description=(
            "Evolution of portfolio sensitivity to "
            f"{benchmark_ticker} through time."
        ),
    )

    st.line_chart(
        rolling_beta,
        use_container_width=True,
    )

    with st.expander(
        "How to interpret market sensitivity"
    ):
        st.write(
            """
            Beta measures how strongly the portfolio historically
            moved relative to the benchmark. A beta above 1 indicates
            greater sensitivity, while a beta below 1 indicates lower
            sensitivity.

            Correlation measures similarity in the direction of
            returns. A portfolio can have low beta but still maintain
            a high correlation with the benchmark.

            Tracking error measures the volatility of returns relative
            to the benchmark. Information Ratio compares active return
            with that tracking error.

            Upside capture measures participation when the benchmark
            rises. Downside capture measures participation when the
            benchmark falls. A high upside capture combined with a
            lower downside capture is generally preferable.
            """
        )