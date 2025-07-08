import streamlit as st
import pandas as pd

import plotly.graph_objects as go


from src.functions.generic_functions import get_all_tickers, get_daily_prices_for_a_ticker
from src.components.charts import candlestick_chart

st.set_page_config("Moving Average Candlestick Chart", layout = "wide")
st.sidebar.header("Select a ticker and a date")

all_tickers = get_all_tickers()

agg_val = None

selected_ticker = st.sidebar.selectbox("Ticker", all_tickers["ticker"].unique())
selected_ticker_name = all_tickers.loc[all_tickers["ticker"] == selected_ticker, "name"].iloc[0]

st.header(f"Moving average candlestick chart for {selected_ticker_name}")

end_date = pd.Timestamp.now().normalize()
start_date = (end_date - pd.Timedelta(days = 150)).normalize()

from_date = st.sidebar.date_input("From", start_date)

to_date = st.sidebar.date_input("To", value = end_date, max_value = end_date)

selected = st.sidebar.multiselect("Select MA", ["5 day MA", "20 day MA", "50 day MA", "200 day MA"], max_selections = 2, default = ["5 day MA", "20 day MA"])

pd_df = get_daily_prices_for_a_ticker(selected_ticker, pd.Timestamp(from_date), pd.Timestamp(to_date))

aggregates_df = pd.json_normalize(pd_df["aggregates"])

result_df = pd.concat([pd_df, aggregates_df], axis = 1).drop("aggregates", axis = 1)


selected_cols = ["date", "open", "high", "low", "close"]
if "5 day MA" in selected:
    selected_cols.append("cumulative_5_day_ma")
if "20 day MA" in selected:
    selected_cols.append("cumulative_20_day_ma")
if "50 day MA" in selected:
    selected_cols.append("cumulative_50_day_ma")
if "200 day MA" in selected:
    selected_cols.append("cumulative_200_day_ma")

agg_val = result_df[selected_cols].copy()

agg_val["date"] = agg_val["date"].dt.strftime("%Y-%m-%d")

agg_val = agg_val.set_index("date").sort_index()

st.dataframe(agg_val, width=1000, height=300)

if agg_val is not None:
    data = candlestick_chart(agg_val, selected)

    fig = go.Figure(data = data)

    fig.update_layout(
        autosize = False, width = 1400, height = 800
    )
    fig.update_xaxes(
        rangebreaks = [
            dict(bounds = ["sat", "mon"])
        ]
    )
    st.plotly_chart(fig)
    