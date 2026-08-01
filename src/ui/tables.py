import pandas as pd
import streamlit as st


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
):
    """
    Renders a consistent financial dataframe.

    percent_columns:
        Decimal values such as 0.125 -> 12.50%

    percentage_point_columns:
        Values already multiplied by 100,
        such as 12.5 -> 12.50%
    """

    if not isinstance(dataframe, pd.DataFrame):
        dataframe = pd.DataFrame(dataframe)

    table_df = dataframe.copy()

    percent_columns = set(percent_columns)
    percentage_point_columns = set(
        percentage_point_columns
    )
    currency_columns = set(currency_columns)
    ratio_columns = set(ratio_columns)
    integer_columns = set(integer_columns)

    column_labels = column_labels or {}

    column_config = {}

    if (
        index_label is not None
        and not hide_index
    ):
        column_config["_index"] = (
            st.column_config.Column(
                index_label,
                width="medium",
            )
        )

    for column in table_df.columns:
        label = column_labels.get(
            column,
            column,
        )

        if column in percent_columns:
            column_config[column] = (
                st.column_config.NumberColumn(
                    label,
                    format="percent",
                    width="small",
                )
            )

        elif column in percentage_point_columns:
            column_config[column] = (
                st.column_config.NumberColumn(
                    label,
                    format="%.2f%%",
                    width="small",
                )
            )

        elif column in currency_columns:
            column_config[column] = (
                st.column_config.NumberColumn(
                    label,
                    format="dollar",
                    width="small",
                )
            )

        elif column in ratio_columns:
            column_config[column] = (
                st.column_config.NumberColumn(
                    label,
                    format="%.2f",
                    width="small",
                )
            )

        elif column in integer_columns:
            column_config[column] = (
                st.column_config.NumberColumn(
                    label,
                    format="%d",
                    width="small",
                )
            )

        elif column in column_labels:
            column_config[column] = (
                st.column_config.Column(
                    label,
                )
            )

    return st.dataframe(
        table_df,
        width="stretch",
        height=height,
        hide_index=hide_index,
        column_config=column_config,
        row_height=36,
        placeholder="—",
        key=key,
    )