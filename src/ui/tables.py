from html import escape
from numbers import Integral, Real

import pandas as pd
import streamlit as st


def format_financial_value(
    column,
    value,
    *,
    percent_columns,
    percentage_point_columns,
    currency_columns,
    ratio_columns,
    integer_columns,
):
    """
    Formats one table value according to its
    financial column category.
    """

    if value is None or pd.isna(value):
        return "—"

    if column in percent_columns:
        return f"{float(value) * 100:.2f}%"

    if column in percentage_point_columns:
        return f"{float(value):.2f}%"

    if column in currency_columns:
        return f"${float(value):,.0f}"

    if column in ratio_columns:
        return f"{float(value):.2f}"

    if column in integer_columns:
        return f"{int(value):,}"

    if isinstance(value, pd.Timestamp):
        return value.strftime("%d %b %Y")

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, Integral):
        return f"{int(value):,}"

    if isinstance(value, Real):
        return f"{float(value):,.2f}"

    return str(value)


def get_default_cell_tone(
    column,
    value,
):
    """
    Assigns restrained positive or negative tones
    only where the financial meaning is clear.
    """

    if value is None or pd.isna(value):
        return ""

    if not isinstance(value, Real):
        return ""

    numeric_value = float(value)
    column_name = str(column).lower()

    risk_terms = (
        "drawdown",
        "value at risk",
        "expected shortfall",
        "cost drag",
        "transaction cost",
    )

    performance_terms = (
        "return",
        "sharpe",
        "information ratio",
    )

    if any(
        term in column_name
        for term in risk_terms
    ):
        if numeric_value != 0:
            return "is-negative"

        return ""

    if any(
        term in column_name
        for term in performance_terms
    ):
        if numeric_value > 0:
            return "is-positive"

        if numeric_value < 0:
            return "is-negative"

    return ""


def render_financial_table(
    dataframe,
    *,
    index_label=None,
    percent_columns=(),
    percentage_point_columns=(),
    currency_columns=(),
    ratio_columns=(),
    integer_columns=(),
    column_labels=None,
    hide_index=False,
    height="auto",
    key=None,
    compact=True,
    tone_resolver=None,
):
    """
    Renders a unified rGraph HTML financial table.

    percent_columns:
        Decimal value: 0.125 -> 12.50%

    percentage_point_columns:
        Already multiplied value: 12.5 -> 12.50%
    """

    if not isinstance(
        dataframe,
        pd.DataFrame,
    ):
        dataframe = pd.DataFrame(
            dataframe
        )

    table_df = dataframe.copy()

    percent_columns = set(
        percent_columns
    )

    percentage_point_columns = set(
        percentage_point_columns
    )

    currency_columns = set(
        currency_columns
    )

    ratio_columns = set(
        ratio_columns
    )

    integer_columns = set(
        integer_columns
    )

    column_labels = (
        column_labels or {}
    )

    if tone_resolver is None:
        tone_resolver = (
            get_default_cell_tone
        )

    table_class = "rg-mc-table"

    if compact:
        table_class += " is-compact"

    scroll_style = ""

    if isinstance(height, int):
        scroll_style = (
            f'max-height: {height}px; '
            "overflow: auto;"
        )

    html_parts = [
        (
            '<div class="rg-mc-table-scroll" '
            f'style="{scroll_style}">'
        ),
        f'<table class="{table_class}">',
        "<thead>",
        "<tr>",
    ]

    if not hide_index:
        resolved_index_label = (
            index_label
            or table_df.index.name
            or "Item"
        )

        html_parts.append(
            f"<th>{escape(str(resolved_index_label))}</th>"
        )

    for column in table_df.columns:
        display_label = column_labels.get(
            column,
            column,
        )

        html_parts.append(
            f"<th>{escape(str(display_label))}</th>"
        )

    html_parts.extend(
        [
            "</tr>",
            "</thead>",
            "<tbody>",
        ]
    )

    for index, row in table_df.iterrows():
        html_parts.append("<tr>")

        if not hide_index:
            html_parts.append(
                f"""
                <th scope="row">
                    {escape(str(index))}
                </th>
                """
            )

        for column in table_df.columns:
            value = row[column]

            formatted_value = (
                format_financial_value(
                    column=column,
                    value=value,
                    percent_columns=(
                        percent_columns
                    ),
                    percentage_point_columns=(
                        percentage_point_columns
                    ),
                    currency_columns=(
                        currency_columns
                    ),
                    ratio_columns=(
                        ratio_columns
                    ),
                    integer_columns=(
                        integer_columns
                    ),
                )
            )

            tone_class = tone_resolver(
                column,
                value,
            )

            html_parts.append(
                f"""
                <td class="{escape(tone_class)}">
                    {escape(str(formatted_value))}
                </td>
                """
            )

        html_parts.append("</tr>")

    html_parts.extend(
        [
            "</tbody>",
            "</table>",
            "</div>",
        ]
    )

    # `key` remains in the signature so existing
    # calls do not need to be changed.
    _ = key

    st.html(
        "".join(html_parts)
    )