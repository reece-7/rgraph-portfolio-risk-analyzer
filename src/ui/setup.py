from html import escape

import streamlit as st


def render_portfolio_setup(
    portfolio_inputs,
    weight_sum,
    duplicate_tickers,
    non_positive_weight_tickers,
    benchmark_ticker,
):
    """
    Renders the current portfolio configuration
    and returns the analysis button state.
    """

    asset_count = len(portfolio_inputs)

    weight_is_valid = abs(weight_sum - 1.0) <= 0.0001
    asset_count_is_valid = asset_count >= 2
    benchmark_is_valid = bool(benchmark_ticker)
    weights_are_positive = not non_positive_weight_tickers

    configuration_is_valid = all(
        [
            weight_is_valid,
            asset_count_is_valid,
            not duplicate_tickers,
            weights_are_positive,
            benchmark_is_valid,
        ]
    )

    issues = []

    if not weight_is_valid:
        issues.append(
            "Portfolio weights must sum to 100%."
        )

    if not asset_count_is_valid:
        issues.append(
            "Enter at least two valid assets."
        )

    if duplicate_tickers:
        issues.append(
            "Each ticker can only be used once."
        )

    if not weights_are_positive:
        issues.append(
            "Every selected asset must have a positive weight."
        )

    if not benchmark_is_valid:
        issues.append(
            "Enter a valid benchmark ticker."
        )

    allocation_rows = []

    for ticker, weight in portfolio_inputs:
        weight_percent = weight * 100

        bar_width = min(
            max(weight_percent, 0.0),
            100.0,
        )

        allocation_rows.append(
            f"""
            <div class="rg-allocation-row">
                <div class="rg-allocation-ticker">
                    {escape(str(ticker))}
                </div>

                <div class="rg-allocation-track">
                    <div
                        class="rg-allocation-fill"
                        style="width: {bar_width:.2f}%"
                    ></div>
                </div>

                <div class="rg-allocation-weight">
                    {weight_percent:.1f}%
                </div>
            </div>
            """
        )

    if allocation_rows:
        allocation_html = "".join(allocation_rows)

    else:
        allocation_html = """
        <div class="rg-allocation-empty">
            Add assets from the sidebar to create an allocation.
        </div>
        """

    if issues:
        issues_html = "".join(
            f"""
            <div class="rg-setup-issue">
                <span>!</span>
                {escape(issue)}
            </div>
            """
            for issue in issues
        )

    else:
        issues_html = """
        <div class="rg-setup-valid">
            <span></span>
            Configuration complete
        </div>
        """

    status_class = (
        "is-valid"
        if configuration_is_valid
        else "is-incomplete"
    )

    status_text = (
        "VALID ALLOCATION"
        if configuration_is_valid
        else "REVIEW INPUTS"
    )

    safe_benchmark = escape(
        benchmark_ticker or "Not selected"
    )

    setup_html = f"""
    <section class="rg-setup">

        <div class="rg-setup-heading">

            <div>
                <div class="rg-section-eyebrow">
                    CURRENT CONFIGURATION
                </div>

                <h2>Portfolio setup</h2>

                <p>
                    Review the allocation before running the
                    portfolio analytics engine.
                </p>
            </div>

            <div class="rg-setup-status {status_class}">
                <span></span>
                {status_text}
            </div>

        </div>

        <div class="rg-setup-meta">

            <div class="rg-setup-meta-item">
                <span>Assets</span>
                <strong>{asset_count}</strong>
            </div>

            <div class="rg-setup-meta-item">
                <span>Total weight</span>
                <strong>{weight_sum * 100:.1f}%</strong>
            </div>

            <div class="rg-setup-meta-item">
                <span>Benchmark</span>
                <strong>{safe_benchmark}</strong>
            </div>

        </div>

        <div class="rg-allocation-list">
            {allocation_html}
        </div>

        <div class="rg-setup-feedback">
            {issues_html}
        </div>

    </section>
    """

    st.html(setup_html)

    action_copy_column, action_button_column = st.columns(
        [3, 1]
    )

    with action_copy_column:
        st.html(
            """
            <div class="rg-analysis-action-copy">
                Generate historical performance, risk simulations,
                optimization and benchmark analytics from the current allocation.
            </div>
            """
        )

    with action_button_column:
        run_button = st.button(
            "Analyze allocation",
            key="run_portfolio_analysis",
            type="tertiary",
            icon=":material/arrow_forward:",
            icon_position="right",
            disabled=not configuration_is_valid,
            width="content",
        )

    return run_button