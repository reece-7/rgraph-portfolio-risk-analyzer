import altair as alt
import numpy as np
import pandas as pd

# Allow charts to use the complete Efficient Frontier dataset.
alt.data_transformers.disable_max_rows()


def apply_rgraph_chart_style(chart):
    """
    Applies the shared rGraph visual language
    to an Altair chart.
    """

    return (
        chart
        .configure(
            background="transparent",
        )
        .configure_view(
            strokeOpacity=0,
        )
        .configure_axis(
            labelColor="#7F98AC",
            titleColor="#9CB1C2",
            gridColor="#20384D",
            gridOpacity=0.45,
            domainColor="#29465E",
            tickColor="#29465E",
            labelFont="Manrope",
            titleFont="Manrope",
            labelFontSize=11,
            titleFontSize=11,
            titleFontWeight=600,
            labelPadding=8,
            titlePadding=14,
        )
        .configure_legend(
            orient="top",
            direction="horizontal",
            titleColor="#71899D",
            labelColor="#A9BBC9",
            titleFont="Manrope",
            labelFont="Manrope",
            titleFontSize=10,
            labelFontSize=10,
            symbolSize=90,
            padding=0,
        )
    )


def build_efficient_frontier_chart(
    efficient_frontier,
    optimal_portfolios,
):
    """
    Builds an interactive Efficient Frontier.

    The Maximum Sharpe and Minimum Volatility
    portfolios are highlighted with stars.
    """

    required_columns = [
        "Annualized Volatility",
        "Annualized Return",
        "Sharpe Ratio",
    ]

    frontier_df = (
        efficient_frontier
        .copy()
        .dropna(subset=required_columns)
        .reset_index(drop=True)
    )

    optimal_df = optimal_portfolios.copy()

    optimal_df["Portfolio"] = (
        optimal_df.index.astype(str)
    )

    portfolio_name_map = {
        "Maximum Sharpe Portfolio": "Maximum Sharpe",
        "Minimum Volatility Portfolio": "Minimum Volatility",
    }

    optimal_df["Display Name"] = (
        optimal_df["Portfolio"]
        .replace(portfolio_name_map)
    )

    if len(optimal_df) >= 1:
        first_index = optimal_df.index[0]

        if (
            optimal_df.loc[first_index, "Display Name"]
            == optimal_df.loc[first_index, "Portfolio"]
        ):
            optimal_df.loc[
                first_index,
                "Display Name",
            ] = "Maximum Sharpe"

    if len(optimal_df) >= 2:
        second_index = optimal_df.index[1]

        if (
            optimal_df.loc[second_index, "Display Name"]
            == optimal_df.loc[second_index, "Portfolio"]
        ):
            optimal_df.loc[
                second_index,
                "Display Name",
            ] = "Minimum Volatility"

    weight_columns = [
        column
        for column in frontier_df.columns
        if column.startswith("Weight ")
    ]

    frontier_tooltips = [
        alt.Tooltip(
            "Annualized Volatility:Q",
            title="Volatility",
            format=".2%",
        ),
        alt.Tooltip(
            "Annualized Return:Q",
            title="Return",
            format=".2%",
        ),
        alt.Tooltip(
            "Sharpe Ratio:Q",
            title="Sharpe Ratio",
            format=".2f",
        ),
    ]

    for column in weight_columns:
        frontier_tooltips.append(
            alt.Tooltip(
                f"{column}:Q",
                title=column.replace("Weight ", ""),
                format=".1%",
            )
        )

    frontier_points = (
        alt.Chart(frontier_df)
        .mark_circle(
            size=42,
            opacity=0.58,
        )
        .encode(
            x=alt.X(
                "Annualized Volatility:Q",
                title="Annualized volatility",
                axis=alt.Axis(
                    format=".0%",
                ),
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            y=alt.Y(
                "Annualized Return:Q",
                title="Annualized return",
                axis=alt.Axis(
                    format=".0%",
                ),
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            color=alt.Color(
                "Sharpe Ratio:Q",
                title="Sharpe ratio",
                scale=alt.Scale(
                    range=[
                        "#29455E",
                        "#35C7FF",
                        "#68DDB2",
                    ]
                ),
            ),
            tooltip=frontier_tooltips,
        )
    )

    optimal_tooltips = [
        alt.Tooltip(
            "Display Name:N",
            title="Portfolio",
        ),
        alt.Tooltip(
            "Annualized Volatility:Q",
            title="Volatility",
            format=".2%",
        ),
        alt.Tooltip(
            "Annualized Return:Q",
            title="Return",
            format=".2%",
        ),
        alt.Tooltip(
            "Sharpe Ratio:Q",
            title="Sharpe Ratio",
            format=".2f",
        ),
    ]

    for column in weight_columns:
        if column in optimal_df.columns:
            optimal_tooltips.append(
                alt.Tooltip(
                    f"{column}:Q",
                    title=column.replace("Weight ", ""),
                    format=".1%",
                )
            )

    optimal_color_scale = alt.Scale(
        domain=[
            "Maximum Sharpe",
            "Minimum Volatility",
        ],
        range=[
            "#FFD166",
            "#FF8FA3",
        ],
    )

    optimal_stars = (
        alt.Chart(optimal_df)
        .mark_text(
            text="★",
            font="Manrope",
            fontSize=27,
            fontWeight=800,
        )
        .encode(
            x=alt.X(
                "Annualized Volatility:Q",
            ),
            y=alt.Y(
                "Annualized Return:Q",
            ),
            color=alt.Color(
                "Display Name:N",
                title="Highlighted portfolio",
                scale=optimal_color_scale,
            ),
            tooltip=optimal_tooltips,
        )
    )

    optimal_labels = (
        alt.Chart(optimal_df)
        .mark_text(
            align="left",
            baseline="bottom",
            dx=14,
            dy=-10,
            font="Manrope",
            fontSize=11,
            fontWeight=600,
        )
        .encode(
            x=alt.X(
                "Annualized Volatility:Q",
            ),
            y=alt.Y(
                "Annualized Return:Q",
            ),
            text=alt.Text(
                "Display Name:N",
            ),
            color=alt.Color(
                "Display Name:N",
                scale=optimal_color_scale,
                legend=None,
            ),
        )
    )

    chart = (
        alt.layer(
            frontier_points,
            optimal_stars,
            optimal_labels,
        )
        .resolve_scale(
            color="independent",
        )
        .properties(
            height=440,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)


def build_allocation_dumbbell_chart(
    weights_comparison,
):
    """
    Compares current and Risk Parity weights
    through a horizontal dumbbell chart.

    Expected values are expressed from 0 to 100.
    """

    comparison_df = (
        weights_comparison
        .copy()
        .reset_index()
    )

    first_column = comparison_df.columns[0]

    comparison_df = comparison_df.rename(
        columns={
            first_column: "Ticker",
        }
    )

    required_columns = [
        "Ticker",
        "Current Portfolio",
        "Risk Parity",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in comparison_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing dumbbell chart columns: "
            + ", ".join(missing_columns)
        )

    comparison_df["Lower Weight"] = (
        comparison_df[
            [
                "Current Portfolio",
                "Risk Parity",
            ]
        ]
        .min(axis=1)
    )

    comparison_df["Upper Weight"] = (
        comparison_df[
            [
                "Current Portfolio",
                "Risk Parity",
            ]
        ]
        .max(axis=1)
    )

    ticker_order = comparison_df[
        "Ticker"
    ].tolist()

    long_df = comparison_df.melt(
        id_vars=["Ticker"],
        value_vars=[
            "Current Portfolio",
            "Risk Parity",
        ],
        var_name="Portfolio",
        value_name="Weight",
    )

    base = alt.Chart(comparison_df).encode(
        y=alt.Y(
            "Ticker:N",
            title=None,
            sort=ticker_order,
            axis=alt.Axis(
                labelFontWeight=600,
            ),
        )
    )

    connecting_lines = (
        base
        .mark_rule(
            color="#38566F",
            strokeWidth=2,
            opacity=0.9,
        )
        .encode(
            x=alt.X(
                "Lower Weight:Q",
                title="Allocation weight",
                axis=alt.Axis(
                    labelExpr="datum.value + '%'",
                ),
                scale=alt.Scale(
                    zero=True,
                ),
            ),
            x2=alt.X2(
                "Upper Weight:Q",
            ),
        )
    )

    allocation_points = (
        alt.Chart(long_df)
        .mark_point(
            filled=True,
            size=135,
            stroke="#07111F",
            strokeWidth=1.5,
        )
        .encode(
            x=alt.X(
                "Weight:Q",
                title="Allocation weight",
                axis=alt.Axis(
                    labelExpr="datum.value + '%'",
                ),
                scale=alt.Scale(
                    zero=True,
                ),
            ),
            y=alt.Y(
                "Ticker:N",
                title=None,
                sort=ticker_order,
            ),
            color=alt.Color(
                "Portfolio:N",
                title=None,
                scale=alt.Scale(
                    domain=[
                        "Current Portfolio",
                        "Risk Parity",
                    ],
                    range=[
                        "#35C7FF",
                        "#68DDB2",
                    ],
                ),
            ),
            shape=alt.Shape(
                "Portfolio:N",
                title=None,
                scale=alt.Scale(
                    domain=[
                        "Current Portfolio",
                        "Risk Parity",
                    ],
                    range=[
                        "circle",
                        "diamond",
                    ],
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Ticker:N",
                    title="Ticker",
                ),
                alt.Tooltip(
                    "Portfolio:N",
                    title="Allocation",
                ),
                alt.Tooltip(
                    "Weight:Q",
                    title="Weight",
                    format=".2f",
                ),
            ],
        )
    )

    current_labels = (
        alt.Chart(
            long_df[
                long_df["Portfolio"]
                == "Current Portfolio"
            ]
        )
        .mark_text(
            align="center",
            baseline="bottom",
            dy=-11,
            font="Manrope",
            fontSize=10,
            fontWeight=600,
            color="#7FD9FF",
        )
        .encode(
            x=alt.X(
                "Weight:Q",
            ),
            y=alt.Y(
                "Ticker:N",
                sort=ticker_order,
            ),
            text=alt.Text(
                "Weight:Q",
                format=".1f",
            ),
        )
    )

    risk_parity_labels = (
        alt.Chart(
            long_df[
                long_df["Portfolio"]
                == "Risk Parity"
            ]
        )
        .mark_text(
            align="center",
            baseline="top",
            dy=12,
            font="Manrope",
            fontSize=10,
            fontWeight=600,
            color="#8BE6C3",
        )
        .encode(
            x=alt.X(
                "Weight:Q",
            ),
            y=alt.Y(
                "Ticker:N",
                sort=ticker_order,
            ),
            text=alt.Text(
                "Weight:Q",
                format=".1f",
            ),
        )
    )

    chart = (
        alt.layer(
            connecting_lines,
            allocation_points,
            current_labels,
            risk_parity_labels,
        )
        .properties(
            height=max(
                260,
                len(ticker_order) * 65,
            ),
        )
    )

    return apply_rgraph_chart_style(chart)

def build_horizontal_allocation_chart(
    allocation_data,
    value_column="Weight (%)",
):
    """
    Builds a horizontal allocation chart with
    background tracks and percentage labels.

    Expected values are expressed from 0 to 100.
    """

    allocation_df = (
        allocation_data
        .copy()
        .reset_index()
    )

    ticker_column = allocation_df.columns[0]

    allocation_df = allocation_df.rename(
        columns={
            ticker_column: "Ticker",
        }
    )

    if value_column not in allocation_df.columns:
        raise ValueError(
            f"Column '{value_column}' was not found."
        )

    allocation_df[value_column] = pd.to_numeric(
        allocation_df[value_column],
        errors="coerce",
    )

    allocation_df = (
        allocation_df
        .dropna(
            subset=[
                "Ticker",
                value_column,
            ]
        )
        .sort_values(
            value_column,
            ascending=False,
        )
    )

    allocation_df["Maximum Weight"] = 100.0
    allocation_df["Label Position"] = 100.0

    ticker_order = allocation_df[
        "Ticker"
    ].tolist()

    background_tracks = (
        alt.Chart(allocation_df)
        .mark_bar(
            color="#13293B",
            size=22,
            cornerRadiusEnd=5,
            opacity=0.85,
        )
        .encode(
            x=alt.X(
                "Maximum Weight:Q",
                title="Portfolio weight",
                scale=alt.Scale(
                    domain=[0, 100],
                ),
                axis=alt.Axis(
                    labelExpr="datum.value + '%'",
                    values=[
                        0,
                        20,
                        40,
                        60,
                        80,
                        100,
                    ],
                ),
            ),
            y=alt.Y(
                "Ticker:N",
                title=None,
                sort=ticker_order,
                axis=alt.Axis(
                    labelFontWeight=600,
                    labelPadding=12,
                ),
            ),
        )
    )

    allocation_bars = (
        alt.Chart(allocation_df)
        .mark_bar(
            color="#35C7FF",
            size=22,
            cornerRadiusEnd=5,
        )
        .encode(
            x=alt.X(
                f"{value_column}:Q",
                title="Portfolio weight",
                scale=alt.Scale(
                    domain=[0, 100],
                ),
                axis=alt.Axis(
                    labelExpr="datum.value + '%'",
                    values=[
                        0,
                        20,
                        40,
                        60,
                        80,
                        100,
                    ],
                ),
            ),
            y=alt.Y(
                "Ticker:N",
                title=None,
                sort=ticker_order,
            ),
            tooltip=[
                alt.Tooltip(
                    "Ticker:N",
                    title="Asset",
                ),
                alt.Tooltip(
                    f"{value_column}:Q",
                    title="Weight",
                    format=".2f",
                ),
            ],
        )
    )

    percentage_labels = (
        alt.Chart(allocation_df)
        .mark_text(
            align="right",
            baseline="middle",
            dx=-2,
            font="Manrope",
            fontSize=11,
            fontWeight=600,
            color="#DCEAF3",
        )
        .encode(
            x=alt.X(
                "Label Position:Q",
                scale=alt.Scale(
                    domain=[0, 100],
                ),
            ),
            y=alt.Y(
                "Ticker:N",
                sort=ticker_order,
            ),
            text=alt.Text(
                f"{value_column}:Q",
                format=".1f",
            ),
        )
    )

    chart = (
        alt.layer(
            background_tracks,
            allocation_bars,
            percentage_labels,
        )
        .properties(
            height=max(
                220,
                len(allocation_df) * 48,
            ),
        )
    )

    return apply_rgraph_chart_style(chart)

def build_strategy_lollipop_chart(
    rebalancing_summary,
):
    """
    Builds a horizontal lollipop chart comparing
    final portfolio values across rebalancing strategies.
    """

    chart_df = (
        rebalancing_summary[
            [
                "Strategy",
                "Final Value",
            ]
        ]
        .copy()
    )

    chart_df["Final Value"] = pd.to_numeric(
        chart_df["Final Value"],
        errors="coerce",
    )

    chart_df = (
        chart_df
        .dropna(
            subset=[
                "Strategy",
                "Final Value",
            ]
        )
        .sort_values(
            "Final Value",
            ascending=False,
        )
    )

    if chart_df.empty:
        raise ValueError(
            "No valid rebalancing values are available."
        )

    best_value = chart_df["Final Value"].max()

    chart_df["Baseline"] = 0.0

    chart_df["Status"] = chart_df[
        "Final Value"
    ].apply(
        lambda value: (
            "Best Strategy"
            if value == best_value
            else "Other Strategy"
        )
    )

    chart_df["Value Label"] = chart_df[
        "Final Value"
    ].map(
        lambda value: f"${value:,.0f}"
    )

    strategy_order = chart_df[
        "Strategy"
    ].tolist()

    maximum_axis_value = max(
        best_value * 1.18,
        1,
    )

    color_scale = alt.Scale(
        domain=[
            "Best Strategy",
            "Other Strategy",
        ],
        range=[
            "#68DDB2",
            "#35C7FF",
        ],
    )

    base = alt.Chart(
        chart_df
    ).encode(
        y=alt.Y(
            "Strategy:N",
            title=None,
            sort=strategy_order,
            axis=alt.Axis(
                labelFontWeight=600,
                labelPadding=12,
            ),
        )
    )

    stems = (
        base
        .mark_rule(
            strokeWidth=3,
            opacity=0.72,
        )
        .encode(
            x=alt.X(
                "Baseline:Q",
                title="Final portfolio value",
                scale=alt.Scale(
                    domain=[
                        0,
                        maximum_axis_value,
                    ],
                ),
                axis=alt.Axis(
                    format="$,.0f",
                ),
            ),
            x2=alt.X2(
                "Final Value:Q",
            ),
            color=alt.Color(
                "Status:N",
                title=None,
                scale=color_scale,
            ),
        )
    )

    endpoints = (
        base
        .mark_circle(
            size=190,
            stroke="#07111F",
            strokeWidth=2,
        )
        .encode(
            x=alt.X(
                "Final Value:Q",
                scale=alt.Scale(
                    domain=[
                        0,
                        maximum_axis_value,
                    ],
                ),
            ),
            color=alt.Color(
                "Status:N",
                title=None,
                scale=color_scale,
            ),
            tooltip=[
                alt.Tooltip(
                    "Strategy:N",
                    title="Strategy",
                ),
                alt.Tooltip(
                    "Final Value:Q",
                    title="Final Value",
                    format="$,.2f",
                ),
                alt.Tooltip(
                    "Status:N",
                    title="Result",
                ),
            ],
        )
    )

    value_labels = (
        base
        .mark_text(
            align="left",
            baseline="middle",
            dx=13,
            font="Manrope",
            fontSize=11,
            fontWeight=600,
            color="#DCE8F1",
        )
        .encode(
            x=alt.X(
                "Final Value:Q",
                scale=alt.Scale(
                    domain=[
                        0,
                        maximum_axis_value,
                    ],
                ),
            ),
            text=alt.Text(
                "Value Label:N",
            ),
        )
    )

    chart = (
        alt.layer(
            stems,
            endpoints,
            value_labels,
        )
        .properties(
            height=max(
                280,
                len(chart_df) * 64,
            ),
        )
    )

    return apply_rgraph_chart_style(chart)


def build_rebalancing_heatmap(
    transaction_cost_summary,
    value_column,
    value_title,
):
    """
    Builds a warm Strategy x Transaction Cost Rate heatmap.
    """

    required_columns = [
        "Strategy",
        "Transaction Cost Rate",
        value_column,
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in transaction_cost_summary.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing heatmap columns: "
            + ", ".join(missing_columns)
        )

    heatmap_df = transaction_cost_summary[
        required_columns
    ].copy()

    heatmap_df[value_column] = pd.to_numeric(
        heatmap_df[value_column],
        errors="coerce",
    )

    heatmap_df["Cost Rate Numeric"] = pd.to_numeric(
        heatmap_df["Transaction Cost Rate"]
        .astype(str)
        .str.replace("%", "", regex=False),
        errors="coerce",
    )

    heatmap_df = (
        heatmap_df
        .dropna(
            subset=[
                "Strategy",
                "Transaction Cost Rate",
                value_column,
            ]
        )
        .groupby(
            [
                "Strategy",
                "Transaction Cost Rate",
                "Cost Rate Numeric",
            ],
            as_index=False,
        )[value_column]
        .mean()
    )

    heatmap_df["Display Value"] = heatmap_df[
        value_column
    ].map(
        lambda value: f"${value:,.0f}"
    )

    cost_rate_order = (
        heatmap_df[
            [
                "Transaction Cost Rate",
                "Cost Rate Numeric",
            ]
        ]
        .drop_duplicates()
        .sort_values("Cost Rate Numeric")[
            "Transaction Cost Rate"
        ]
        .tolist()
    )

    preferred_strategy_order = [
        "Buy & Hold",
        "Monthly Rebalancing",
        "Quarterly Rebalancing",
        "Annual Rebalancing",
    ]

    available_strategies = (
        heatmap_df["Strategy"]
        .drop_duplicates()
        .tolist()
    )

    strategy_order = [
        strategy
        for strategy in preferred_strategy_order
        if strategy in available_strategies
    ]

    strategy_order.extend(
        strategy
        for strategy in available_strategies
        if strategy not in strategy_order
    )

    maximum_value = heatmap_df[value_column].max()

    text_threshold = (
        maximum_value * 0.55
        if maximum_value > 0
        else 0
    )

    base = alt.Chart(
        heatmap_df
    ).encode(
        x=alt.X(
            "Transaction Cost Rate:N",
            title="Transaction cost rate",
            sort=cost_rate_order,
            axis=alt.Axis(
                labelAngle=0,
                labelPadding=10,
            ),
        ),
        y=alt.Y(
            "Strategy:N",
            title=None,
            sort=strategy_order,
            axis=alt.Axis(
                labelFontWeight=600,
                labelPadding=12,
            ),
        ),
    )

    cells = (
        base
        .mark_rect(
            stroke="#07111F",
            strokeWidth=3,
        )
        .encode(
            color=alt.Color(
                f"{value_column}:Q",
                title=value_title,
                scale=alt.Scale(
                    domainMin=0,
                    range=[
                        "#0B1724",
                        "#12304A",
                        "#17577A",
                        "#168EAA",
                        "#35C7FF",
                        "#68DDB2",
                    ],
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Strategy:N",
                    title="Strategy",
                ),
                alt.Tooltip(
                    "Transaction Cost Rate:N",
                    title="Cost rate",
                ),
                alt.Tooltip(
                    f"{value_column}:Q",
                    title=value_title,
                    format="$,.2f",
                ),
            ],
        )
    )

    labels = (
        base
        .mark_text(
            font="Manrope",
            fontSize=11,
            fontWeight=600,
        )
        .encode(
            text=alt.Text(
                "Display Value:N",
            ),
            color=alt.condition(
                f"datum['{value_column}'] >= {text_threshold}",
                alt.value("#07111F"),
                alt.value("#DCE8F1"),
            ),
        )
    )

    chart = (
        alt.layer(
            cells,
            labels,
        )
        .properties(
            height=max(
                290,
                len(strategy_order) * 68,
            ),
        )
    )

    return apply_rgraph_chart_style(chart)

def build_terminal_distribution_chart(
    parametric_values,
    bootstrap_values,
    initial_value,
    bins=45,
):
    """
    Builds an overlaid terminal-value distribution chart
    for parametric and bootstrap Monte Carlo simulations.
    """

    parametric_values = np.asarray(
        parametric_values,
        dtype=float,
    )

    bootstrap_values = np.asarray(
        bootstrap_values,
        dtype=float,
    )

    parametric_values = parametric_values[
        np.isfinite(parametric_values)
    ]

    bootstrap_values = bootstrap_values[
        np.isfinite(bootstrap_values)
    ]

    if (
        len(parametric_values) == 0
        or len(bootstrap_values) == 0
    ):
        raise ValueError(
            "Monte Carlo terminal values are not available."
        )

    combined_values = np.concatenate(
        [
            parametric_values,
            bootstrap_values,
        ]
    )

    lower_bound = combined_values.min()
    upper_bound = combined_values.max()

    if lower_bound == upper_bound:
        upper_bound = lower_bound + 1

    bin_edges = np.linspace(
        lower_bound,
        upper_bound,
        bins + 1,
    )

    parametric_counts, _ = np.histogram(
        parametric_values,
        bins=bin_edges,
    )

    bootstrap_counts, _ = np.histogram(
        bootstrap_values,
        bins=bin_edges,
    )

    bin_centers = (
        bin_edges[:-1]
        + bin_edges[1:]
    ) / 2

    parametric_df = pd.DataFrame(
        {
            "Final Value": bin_centers,
            "Bin Start": bin_edges[:-1],
            "Bin End": bin_edges[1:],
            "Share": (
                parametric_counts
                / len(parametric_values)
                * 100
            ),
            "Model": "Parametric",
        }
    )

    bootstrap_df = pd.DataFrame(
        {
            "Final Value": bin_centers,
            "Bin Start": bin_edges[:-1],
            "Bin End": bin_edges[1:],
            "Share": (
                bootstrap_counts
                / len(bootstrap_values)
                * 100
            ),
            "Model": "Bootstrap",
        }
    )

    distribution_df = pd.concat(
        [
            parametric_df,
            bootstrap_df,
        ],
        ignore_index=True,
    )

    model_scale = alt.Scale(
        domain=[
            "Parametric",
            "Bootstrap",
        ],
        range=[
            "#35C7FF",
            "#68DDB2",
        ],
    )

    base = (
        alt.Chart(distribution_df)
        .encode(
            x=alt.X(
                "Final Value:Q",
                title="Terminal portfolio value",
                axis=alt.Axis(
                    format="$,.0f",
                ),
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            y=alt.Y(
                "Share:Q",
                title="Share of simulations",
                axis=alt.Axis(
                    labelExpr="datum.value + '%'",
                ),
            ),
            color=alt.Color(
                "Model:N",
                title=None,
                scale=model_scale,
            ),
        )
    )

    distribution_areas = (
        base
        .mark_area(
            opacity=0.18,
            interpolate="monotone",
        )
    )

    distribution_lines = (
        base
        .mark_line(
            strokeWidth=2.4,
            interpolate="monotone",
        )
        .encode(
            tooltip=[
                alt.Tooltip(
                    "Model:N",
                    title="Model",
                ),
                alt.Tooltip(
                    "Bin Start:Q",
                    title="Range from",
                    format="$,.0f",
                ),
                alt.Tooltip(
                    "Bin End:Q",
                    title="Range to",
                    format="$,.0f",
                ),
                alt.Tooltip(
                    "Share:Q",
                    title="Simulations",
                    format=".2f",
                ),
            ]
        )
    )

    reference_df = pd.DataFrame(
        {
            "Reference": [
                "Initial Capital",
                "Parametric Median",
                "Bootstrap Median",
            ],
            "Value": [
                float(initial_value),
                float(np.median(parametric_values)),
                float(np.median(bootstrap_values)),
            ],
        }
    )

    reference_scale = alt.Scale(
        domain=[
            "Initial Capital",
            "Parametric Median",
            "Bootstrap Median",
        ],
        range=[
            "#F4C95D",
            "#35C7FF",
            "#68DDB2",
        ],
    )

    reference_rules = (
        alt.Chart(reference_df)
        .mark_rule(
            strokeWidth=1.8,
            strokeDash=[6, 5],
        )
        .encode(
            x=alt.X("Value:Q"),
            color=alt.Color(
                "Reference:N",
                title="Reference",
                scale=reference_scale,
            ),
            tooltip=[
                alt.Tooltip(
                    "Reference:N",
                    title="Reference",
                ),
                alt.Tooltip(
                    "Value:Q",
                    title="Value",
                    format="$,.2f",
                ),
            ],
        )
    )

    chart = (
        alt.layer(
            distribution_areas,
            distribution_lines,
            reference_rules,
        )
        .resolve_scale(
            color="independent",
        )
        .properties(
            height=420,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)

def build_monte_carlo_fan_chart(
    paths_df,
    fan_chart_lines,
    initial_value,
    model_name,
    accent_color,
):
    """
    Builds a Monte Carlo fan chart using percentile bands.

    paths_df must have:
    - rows: forecast days
    - columns: individual simulations
    """

    paths_df = paths_df.copy()

    percentile_df = pd.DataFrame(
        {
            "Day": np.arange(
                1,
                len(paths_df) + 1,
            ),
            "P05": paths_df.quantile(
                0.05,
                axis=1,
            ).to_numpy(),
            "P25": paths_df.quantile(
                0.25,
                axis=1,
            ).to_numpy(),
            "Median": paths_df.quantile(
                0.50,
                axis=1,
            ).to_numpy(),
            "P75": paths_df.quantile(
                0.75,
                axis=1,
            ).to_numpy(),
            "P95": paths_df.quantile(
                0.95,
                axis=1,
            ).to_numpy(),
        }
    )

    initial_row = pd.DataFrame(
        {
            "Day": [0],
            "P05": [initial_value],
            "P25": [initial_value],
            "Median": [initial_value],
            "P75": [initial_value],
            "P95": [initial_value],
        }
    )

    percentile_df = pd.concat(
        [
            initial_row,
            percentile_df,
        ],
        ignore_index=True,
    )

    base = alt.Chart(
        percentile_df
    ).encode(
        x=alt.X(
            "Day:Q",
            title="Forecast day",
            axis=alt.Axis(
                tickMinStep=1,
            ),
        )
    )

    chart_layers = []

    # =========================
    # OUTER 5–95% BAND
    # =========================

    if fan_chart_lines == 5:
        outer_band = (
            base
            .mark_area(
                color=accent_color,
                opacity=0.10,
                interpolate="monotone",
            )
            .encode(
                y=alt.Y(
                    "P05:Q",
                    title="Portfolio value",
                    axis=alt.Axis(
                        format="$,.0f",
                    ),
                    scale=alt.Scale(
                        zero=False,
                    ),
                ),
                y2=alt.Y2(
                    "P95:Q",
                ),
                tooltip=[
                    alt.Tooltip(
                        "Day:Q",
                        title="Forecast day",
                        format=".0f",
                    ),
                    alt.Tooltip(
                        "P05:Q",
                        title="5th percentile",
                        format="$,.0f",
                    ),
                    alt.Tooltip(
                        "P95:Q",
                        title="95th percentile",
                        format="$,.0f",
                    ),
                ],
            )
        )

        outer_lower_line = (
            base
            .mark_line(
                color=accent_color,
                opacity=0.30,
                strokeWidth=1,
                strokeDash=[4, 5],
                interpolate="monotone",
            )
            .encode(
                y=alt.Y(
                    "P05:Q",
                    scale=alt.Scale(
                        zero=False,
                    ),
                )
            )
        )

        outer_upper_line = (
            base
            .mark_line(
                color=accent_color,
                opacity=0.30,
                strokeWidth=1,
                strokeDash=[4, 5],
                interpolate="monotone",
            )
            .encode(
                y=alt.Y(
                    "P95:Q",
                    scale=alt.Scale(
                        zero=False,
                    ),
                )
            )
        )

        chart_layers.extend(
            [
                outer_band,
                outer_lower_line,
                outer_upper_line,
            ]
        )

    # =========================
    # INNER 25–75% BAND
    # =========================

    if fan_chart_lines in [3, 5]:
        inner_band = (
            base
            .mark_area(
                color=accent_color,
                opacity=0.23,
                interpolate="monotone",
            )
            .encode(
                y=alt.Y(
                    "P25:Q",
                    title="Portfolio value",
                    axis=alt.Axis(
                        format="$,.0f",
                    ),
                    scale=alt.Scale(
                        zero=False,
                    ),
                ),
                y2=alt.Y2(
                    "P75:Q",
                ),
                tooltip=[
                    alt.Tooltip(
                        "Day:Q",
                        title="Forecast day",
                        format=".0f",
                    ),
                    alt.Tooltip(
                        "P25:Q",
                        title="25th percentile",
                        format="$,.0f",
                    ),
                    alt.Tooltip(
                        "Median:Q",
                        title="Median",
                        format="$,.0f",
                    ),
                    alt.Tooltip(
                        "P75:Q",
                        title="75th percentile",
                        format="$,.0f",
                    ),
                ],
            )
        )

        inner_lower_line = (
            base
            .mark_line(
                color=accent_color,
                opacity=0.48,
                strokeWidth=1.1,
                interpolate="monotone",
            )
            .encode(
                y=alt.Y(
                    "P25:Q",
                    scale=alt.Scale(
                        zero=False,
                    ),
                )
            )
        )

        inner_upper_line = (
            base
            .mark_line(
                color=accent_color,
                opacity=0.48,
                strokeWidth=1.1,
                interpolate="monotone",
            )
            .encode(
                y=alt.Y(
                    "P75:Q",
                    scale=alt.Scale(
                        zero=False,
                    ),
                )
            )
        )

        chart_layers.extend(
            [
                inner_band,
                inner_lower_line,
                inner_upper_line,
            ]
        )

    # =========================
    # MEDIAN
    # =========================

    median_line = (
        base
        .mark_line(
            color=accent_color,
            strokeWidth=2.8,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Median:Q",
                title="Portfolio value",
                axis=alt.Axis(
                    format="$,.0f",
                ),
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Day:Q",
                    title="Forecast day",
                    format=".0f",
                ),
                alt.Tooltip(
                    "Median:Q",
                    title=f"{model_name} median",
                    format="$,.0f",
                ),
            ],
        )
    )

    chart_layers.append(
        median_line
    )

    # =========================
    # INITIAL CAPITAL
    # =========================

    initial_capital_df = pd.DataFrame(
        {
            "Initial Capital": [
                float(initial_value)
            ]
        }
    )

    initial_capital_rule = (
        alt.Chart(initial_capital_df)
        .mark_rule(
            color="#F4C95D",
            opacity=0.78,
            strokeWidth=1.3,
            strokeDash=[6, 5],
        )
        .encode(
            y=alt.Y(
                "Initial Capital:Q",
            ),
            tooltip=[
                alt.Tooltip(
                    "Initial Capital:Q",
                    title="Initial capital",
                    format="$,.0f",
                )
            ],
        )
    )

    chart_layers.append(
        initial_capital_rule
    )

    chart = (
        alt.layer(
            *chart_layers
        )
        .properties(
            height=410,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)

def build_performance_value_chart(
    portfolio_values,
):
    """
    Builds the historical portfolio value chart.
    """

    chart_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                portfolio_values.index
            ),
            "Portfolio Value": pd.to_numeric(
                portfolio_values.to_numpy(),
                errors="coerce",
            ),
        }
    ).dropna()

    base = (
        alt.Chart(chart_df)
        .encode(
            x=alt.X(
                "Date:T",
                title=None,
                axis=alt.Axis(
                    format="%b %Y",
                    labelAngle=0,
                ),
            )
        )
    )

    value_area = (
        base
        .mark_area(
            color="#35C7FF",
            opacity=0.10,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Portfolio Value:Q",
                title="Portfolio value",
                axis=alt.Axis(
                    format="$,.0f",
                ),
                scale=alt.Scale(
                    zero=False,
                ),
            )
        )
    )

    value_line = (
        base
        .mark_line(
            color="#35C7FF",
            strokeWidth=2.3,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Portfolio Value:Q",
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Portfolio Value:Q",
                    title="Portfolio value",
                    format="$,.2f",
                ),
            ],
        )
    )

    latest_point = (
        alt.Chart(
            chart_df.tail(1)
        )
        .mark_circle(
            color="#68DDB2",
            size=90,
            stroke="#07111F",
            strokeWidth=2,
        )
        .encode(
            x=alt.X(
                "Date:T",
            ),
            y=alt.Y(
                "Portfolio Value:Q",
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Latest date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Portfolio Value:Q",
                    title="Latest value",
                    format="$,.2f",
                ),
            ],
        )
    )

    chart = (
        alt.layer(
            value_area,
            value_line,
            latest_point,
        )
        .properties(
            height=390,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)


def build_drawdown_chart(
    drawdowns,
):
    """
    Builds the historical drawdown area chart.
    """

    chart_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                drawdowns.index
            ),
            "Drawdown": pd.to_numeric(
                drawdowns.to_numpy(),
                errors="coerce",
            ),
        }
    ).dropna()

    base = (
        alt.Chart(chart_df)
        .encode(
            x=alt.X(
                "Date:T",
                title=None,
                axis=alt.Axis(
                    format="%b %Y",
                    labelAngle=0,
                ),
            )
        )
    )

    drawdown_area = (
        base
        .mark_area(
            color="#35C7FF",
            opacity=0.18,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Drawdown:Q",
                title="Drawdown",
                axis=alt.Axis(
                    format=".0%",
                ),
                scale=alt.Scale(
                    zero=True,
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Drawdown:Q",
                    title="Drawdown",
                    format=".2%",
                ),
            ],
        )
    )

    drawdown_line = (
        base
        .mark_line(
            color="#35C7FF",
            strokeWidth=1.5,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Drawdown:Q",
                scale=alt.Scale(
                    zero=True,
                ),
            )
        )
    )

    zero_reference = (
        alt.Chart(
            pd.DataFrame(
                {
                    "Zero": [0.0],
                }
            )
        )
        .mark_rule(
            color="#6686A8",
            opacity=0.75,
            strokeWidth=1,
        )
        .encode(
            y=alt.Y(
                "Zero:Q",
            )
        )
    )

    chart = (
        alt.layer(
            drawdown_area,
            drawdown_line,
            zero_reference,
        )
        .properties(
            height=350,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)


def build_daily_returns_chart(
    portfolio_returns,
):
    """
    Builds a daily return bar chart with a zero reference.
    """

    chart_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                portfolio_returns.index
            ),
            "Daily Return": pd.to_numeric(
                portfolio_returns.to_numpy(),
                errors="coerce",
            ),
        }
    ).dropna()

    return_bars = (
        alt.Chart(chart_df)
        .mark_bar(
            opacity=0.76,
        )
        .encode(
            x=alt.X(
                "Date:T",
                title=None,
                axis=alt.Axis(
                    format="%b %Y",
                    labelAngle=0,
                ),
            ),
            y=alt.Y(
                "Daily Return:Q",
                title="Daily return",
                axis=alt.Axis(
                    format=".1%",
                ),
            ),
            color=alt.condition(
                alt.datum["Daily Return"] >= 0,
                alt.value("#68DDB2"),
                alt.value("#FF7B8B"),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Daily Return:Q",
                    title="Daily return",
                    format=".2%",
                ),
            ],
        )
    )

    zero_reference = (
        alt.Chart(
            pd.DataFrame(
                {
                    "Zero": [0.0],
                }
            )
        )
        .mark_rule(
            color="#7F98AC",
            opacity=0.75,
            strokeWidth=1,
        )
        .encode(
            y=alt.Y(
                "Zero:Q",
            )
        )
    )

    chart = (
        alt.layer(
            return_bars,
            zero_reference,
        )
        .properties(
            height=350,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)

def build_market_growth_chart(
    normalized_growth,
    benchmark_ticker,
):
    """
    Compares the growth of 100 invested in the
    portfolio and in the selected benchmark.
    """

    chart_df = normalized_growth.copy()

    chart_df.index = pd.to_datetime(
        chart_df.index
    )

    chart_df.index.name = "Date"

    chart_df = (
        chart_df
        .reset_index()
        .melt(
            id_vars="Date",
            var_name="Series",
            value_name="Indexed Value",
        )
        .dropna()
    )

    series_order = [
        "Portfolio",
        benchmark_ticker,
    ]

    color_scale = alt.Scale(
        domain=series_order,
        range=[
            "#35C7FF",
            "#68DDB2",
        ],
    )

    base = alt.Chart(
        chart_df
    ).encode(
        x=alt.X(
            "Date:T",
            title=None,
            axis=alt.Axis(
                format="%b %Y",
                labelAngle=0,
            ),
        ),
        color=alt.Color(
            "Series:N",
            title=None,
            sort=series_order,
            scale=color_scale,
        ),
    )

    growth_lines = (
        base
        .mark_line(
            strokeWidth=2.2,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Indexed Value:Q",
                title="Growth of 100",
                axis=alt.Axis(
                    format=".0f",
                ),
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Series:N",
                    title="Series",
                ),
                alt.Tooltip(
                    "Indexed Value:Q",
                    title="Indexed value",
                    format=".2f",
                ),
            ],
        )
    )

    latest_date = chart_df["Date"].max()

    latest_points_df = chart_df[
        chart_df["Date"] == latest_date
    ]

    latest_points = (
        alt.Chart(latest_points_df)
        .mark_circle(
            size=85,
            stroke="#07111F",
            strokeWidth=2,
        )
        .encode(
            x=alt.X(
                "Date:T",
            ),
            y=alt.Y(
                "Indexed Value:Q",
            ),
            color=alt.Color(
                "Series:N",
                scale=color_scale,
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(
                    "Series:N",
                    title="Series",
                ),
                alt.Tooltip(
                    "Date:T",
                    title="Latest date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Indexed Value:Q",
                    title="Latest indexed value",
                    format=".2f",
                ),
            ],
        )
    )

    initial_reference = (
        alt.Chart(
            pd.DataFrame(
                {
                    "Initial Value": [100.0],
                }
            )
        )
        .mark_rule(
            color="#6686A8",
            opacity=0.65,
            strokeWidth=1,
            strokeDash=[5, 5],
        )
        .encode(
            y=alt.Y(
                "Initial Value:Q",
            ),
            tooltip=[
                alt.Tooltip(
                    "Initial Value:Q",
                    title="Starting level",
                    format=".0f",
                )
            ],
        )
    )

    chart = (
        alt.layer(
            initial_reference,
            growth_lines,
            latest_points,
        )
        .properties(
            height=390,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)


def build_rolling_beta_chart(
    rolling_beta,
    benchmark_ticker,
):
    """
    Displays the evolution of rolling portfolio beta.
    """

    if isinstance(
        rolling_beta,
        pd.DataFrame,
    ):
        if rolling_beta.shape[1] == 0:
            beta_series = pd.Series(
                dtype=float
            )

        else:
            beta_series = (
                rolling_beta
                .iloc[:, 0]
                .copy()
            )

    else:
        beta_series = pd.Series(
            rolling_beta
        ).copy()

    beta_series = (
        pd.to_numeric(
            beta_series,
            errors="coerce",
        )
        .dropna()
    )

    chart_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                beta_series.index
            ),
            "Rolling Beta": (
                beta_series.to_numpy()
            ),
        }
    ).dropna()

    base = alt.Chart(
        chart_df
    ).encode(
        x=alt.X(
            "Date:T",
            title=None,
            axis=alt.Axis(
                format="%b %Y",
                labelAngle=0,
            ),
        )
    )

    beta_area = (
        base
        .mark_area(
            color="#35C7FF",
            opacity=0.09,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Rolling Beta:Q",
                title=f"Beta vs {benchmark_ticker}",
                scale=alt.Scale(
                    zero=False,
                ),
            )
        )
    )

    beta_line = (
        base
        .mark_line(
            color="#35C7FF",
            strokeWidth=2.1,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Rolling Beta:Q",
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Rolling Beta:Q",
                    title="Rolling beta",
                    format=".2f",
                ),
            ],
        )
    )

    market_beta_reference = (
        alt.Chart(
            pd.DataFrame(
                {
                    "Market Beta": [1.0],
                }
            )
        )
        .mark_rule(
            color="#68DDB2",
            opacity=0.7,
            strokeWidth=1.2,
            strokeDash=[6, 5],
        )
        .encode(
            y=alt.Y(
                "Market Beta:Q",
            ),
            tooltip=[
                alt.Tooltip(
                    "Market Beta:Q",
                    title="Market-equivalent beta",
                    format=".1f",
                )
            ],
        )
    )

    chart_layers = [
        market_beta_reference,
        beta_area,
        beta_line,
    ]

    if not chart_df.empty:
        latest_point = (
            alt.Chart(
                chart_df.tail(1)
            )
            .mark_circle(
                color="#68DDB2",
                size=90,
                stroke="#07111F",
                strokeWidth=2,
            )
            .encode(
                x=alt.X(
                    "Date:T",
                ),
                y=alt.Y(
                    "Rolling Beta:Q",
                ),
                tooltip=[
                    alt.Tooltip(
                        "Date:T",
                        title="Latest date",
                        format="%d %b %Y",
                    ),
                    alt.Tooltip(
                        "Rolling Beta:Q",
                        title="Latest rolling beta",
                        format=".2f",
                    ),
                ],
            )
        )

        chart_layers.append(
            latest_point
        )

    chart = (
        alt.layer(
            *chart_layers
        )
        .properties(
            height=360,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)

def build_rebalancing_paths_chart(
    strategy_paths,
):
    """
    Compares historical portfolio values across
    rebalancing strategies.
    """

    chart_df = strategy_paths.copy()

    chart_df.index = pd.to_datetime(
        chart_df.index
    )

    chart_df.index.name = "Date"

    chart_df = (
        chart_df
        .reset_index()
        .melt(
            id_vars="Date",
            var_name="Strategy",
            value_name="Portfolio Value",
        )
        .dropna()
    )

    preferred_order = [
        "Buy & Hold",
        "Monthly Rebalancing",
        "Quarterly Rebalancing",
        "Annual Rebalancing",
    ]

    available_strategies = (
        chart_df["Strategy"]
        .drop_duplicates()
        .tolist()
    )

    strategy_order = [
        strategy
        for strategy in preferred_order
        if strategy in available_strategies
    ]

    strategy_order.extend(
        strategy
        for strategy in available_strategies
        if strategy not in strategy_order
    )

    strategy_colors = [
        "#35C7FF",
        "#68DDB2",
        "#4E8FD5",
        "#8FB9D8",
        "#6F9FBF",
        "#A7CADF",
    ]

    color_scale = alt.Scale(
        domain=strategy_order,
        range=strategy_colors[
            :len(strategy_order)
        ],
    )

    base = alt.Chart(
        chart_df
    ).encode(
        x=alt.X(
            "Date:T",
            title=None,
            axis=alt.Axis(
                format="%b %Y",
                labelAngle=0,
            ),
        ),
        color=alt.Color(
            "Strategy:N",
            title=None,
            sort=strategy_order,
            scale=color_scale,
        ),
    )

    strategy_lines = (
        base
        .mark_line(
            strokeWidth=2.1,
            interpolate="monotone",
        )
        .encode(
            y=alt.Y(
                "Portfolio Value:Q",
                title="Portfolio value",
                axis=alt.Axis(
                    format="$,.0f",
                ),
                scale=alt.Scale(
                    zero=False,
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Strategy:N",
                    title="Strategy",
                ),
                alt.Tooltip(
                    "Portfolio Value:Q",
                    title="Portfolio value",
                    format="$,.2f",
                ),
            ],
        )
    )

    latest_date = chart_df["Date"].max()

    latest_values = chart_df[
        chart_df["Date"] == latest_date
    ]

    latest_points = (
        alt.Chart(latest_values)
        .mark_circle(
            size=85,
            stroke="#07111F",
            strokeWidth=2,
        )
        .encode(
            x=alt.X(
                "Date:T",
            ),
            y=alt.Y(
                "Portfolio Value:Q",
            ),
            color=alt.Color(
                "Strategy:N",
                scale=color_scale,
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(
                    "Strategy:N",
                    title="Strategy",
                ),
                alt.Tooltip(
                    "Date:T",
                    title="Latest date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Portfolio Value:Q",
                    title="Final value",
                    format="$,.2f",
                ),
            ],
        )
    )

    chart = (
        alt.layer(
            strategy_lines,
            latest_points,
        )
        .properties(
            height=390,
        )
        .interactive()
    )

    return apply_rgraph_chart_style(chart)