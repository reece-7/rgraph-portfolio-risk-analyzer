import altair as alt
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
    Builds a Strategy x Transaction Cost Rate heatmap.

    Used for Cost Drag and Total Transaction Costs.
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

    heatmap_df = (
        transaction_cost_summary[
            required_columns
        ]
        .copy()
    )

    heatmap_df[value_column] = pd.to_numeric(
        heatmap_df[value_column],
        errors="coerce",
    )

    heatmap_df["Cost Rate Numeric"] = (
        heatmap_df["Transaction Cost Rate"]
        .astype(str)
        .str.replace(
            "%",
            "",
            regex=False,
        )
        .pipe(
            pd.to_numeric,
            errors="coerce",
        )
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

    maximum_value = heatmap_df[
        value_column
    ].max()

    text_threshold = (
        maximum_value * 0.58
        if maximum_value > 0
        else 0
    )

    heatmap_df["Text Color"] = heatmap_df[
        value_column
    ].apply(
        lambda value: (
            "#07111F"
            if value >= text_threshold
            and maximum_value > 0
            else "#DCE8F1"
        )
    )

    cost_rate_order = (
        heatmap_df[
            [
                "Transaction Cost Rate",
                "Cost Rate Numeric",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            "Cost Rate Numeric"
        )[
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

    available_strategies = heatmap_df[
        "Strategy"
    ].drop_duplicates().tolist()

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
            cornerRadius=5,
            stroke="#07111F",
            strokeWidth=3,
        )
        .encode(
            color=alt.Color(
                f"{value_column}:Q",
                title=value_title,
                scale=alt.Scale(
                    range=[
                        "#102131",
                        "#17445A",
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
                    title="Cost Rate",
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
            baseline="middle",
            font="Manrope",
            fontSize=11,
            fontWeight=600,
        )
        .encode(
            text=alt.Text(
                "Display Value:N",
            ),
            color=alt.Color(
                "Text Color:N",
                scale=None,
                legend=None,
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