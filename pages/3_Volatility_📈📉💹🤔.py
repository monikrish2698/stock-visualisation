import streamlit as st
import pandas as pd

import plotly.graph_objects as go


from src.functions.generic_functions import get_volatility_tickers, get_ticker_details

st.set_page_config("Annulaised Volatility by Industry", layout = "wide")
st.sidebar.header("Select an industry")

all_tickers = get_volatility_tickers()

ticker_details_df = get_ticker_details()

ticker_details_df = ticker_details_df.loc[ticker_details_df["market_cap_size"] != 'Small Cap']

merged_df = pd.merge(all_tickers, ticker_details_df, on = "ticker", how = "inner")

selected_industry = st.sidebar.selectbox("Industry", merged_df["sic_description"].unique())

st.header(f"Sentiment and Annulaised Volatility for {selected_industry}")

volatility_df = merged_df.loc[merged_df["sic_description"] == selected_industry, ["annualised_7d_volatility", "annualised_30d_volatility", "date"]]

volatility_grouped_df = volatility_df.groupby("date").agg({"annualised_7d_volatility": "mean", "annualised_30d_volatility": "mean"}).reset_index()

volatility_grouped_df["date"] = volatility_grouped_df["date"].dt.strftime("%Y-%m-%d")
volatility_grouped_df = volatility_grouped_df.set_index("date").sort_index()

colors = ["#26a69a" if h >= 0 else "#ef5350" for h in volatility_grouped_df["annualised_7d_volatility"]]

fig_dist = go.Figure(
    data = [
        go.Scatter(
            x=volatility_grouped_df.index,
            y=volatility_grouped_df.annualised_7d_volatility,
            line=dict(color="blue", width=2),
            name="Annualised 7d Volatility"),
        go.Scatter(
            x=volatility_grouped_df.index,
            y=volatility_grouped_df.annualised_30d_volatility,
            line=dict(color="red", width=2),
            name="Annualised 30d Volatility")
        ]

    )
fig_dist.update_xaxes(
    rangebreaks = [
        dict(bounds = ["sat", "mon"])
    ]
)

fig_dist.update_yaxes(
    range=[0, 100],
    autorange=False
)

st.plotly_chart(fig_dist)
