import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go

from src.functions.generic_functions import get_macd_for_a_ticker, get_all_macd_tickers, get_all_tickers, get_ema_for_a_ticker
from src.components.charts import candlestick_chart

st.set_page_config("Moving Average Convergence Divergence (MACD)", layout = "wide")
st.sidebar.header("Select a ticker")

all_tickers = get_all_tickers()
macd_tickers = get_all_macd_tickers()
merged = pd.merge(all_tickers, macd_tickers, on = "ticker", how = "inner")

selected_ticker = st.sidebar.selectbox("Ticker", merged["ticker"].unique())
selected_ticker_name = merged.loc[merged["ticker"] == selected_ticker, "name"].iloc[0]

st.header(f"Exponential Moving Averages Candlestick Chart for {selected_ticker_name}")

macd_df = get_macd_for_a_ticker(selected_ticker)

macd_df["date"] = macd_df["date"].dt.strftime("%Y-%m-%d")

macd_df = macd_df.set_index("date").sort_index()

ema_df = get_ema_for_a_ticker(selected_ticker)
aggregates_df = pd.json_normalize(ema_df["aggregates"])

result_df = pd.concat([ema_df, aggregates_df], axis = 1).drop("aggregates", axis = 1)

result_df["date"] = result_df["date"].dt.strftime("%Y-%m-%d")
result_df = result_df.set_index("date").sort_index()

data = candlestick_chart(result_df, [])

data.append(
    go.Scatter(
        x = result_df.index,
        y = result_df.ema_12_day,
        line=dict(color="blue", width=2),
        name = "EMA 12 Day")
)

data.append(
    go.Scatter(
        x = result_df.index,
        y = result_df.ema_26_day,
        line=dict(color="red", width=2),
        name = "EMA 26 Day")
)

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

colors = ["#26a69a" if h >= 0 else "#ef5350" for h in macd_df["histogram"]]

st.header(f"MACD for {selected_ticker_name}")

fig_dist = go.Figure(
    data = [
        go.Bar(
            x=macd_df.index,
            y=macd_df.histogram,
            marker_color=colors,
            name="Histogram"),
        go.Scatter(
            x = macd_df.index,
            y = macd_df.macd_line,
            line=dict(color="blue", width=2),
            name = "MACD Line"),
        go.Scatter(
            x = macd_df.index,
            y = macd_df.signal_line,
            line=dict(color="red", width=2),
            name = "Signal Line")
        ]
    )
fig_dist.update_layout(
    xaxis_title="Date",
    yaxis_title="Value",
    showlegend=True,
    bargap=0,
    template="plotly_white"
)
fig_dist.update_yaxes(
    zeroline=True,
    zerolinewidth=1,
    zerolinecolor="black"
)
fig_dist.update_xaxes(
    rangebreaks = [
        dict(bounds = ["sat", "mon"])
    ]
)

bull_sig = macd_df.loc[
    macd_df.signal_line_crossover == "bullish_signal_cross"]
bear_sig = macd_df.loc[
    macd_df.signal_line_crossover == "bearish_signal_cross"]

bull_zero = macd_df.loc[
    macd_df.zero_crossover == "bullish_zero_cross"]
bear_zero = macd_df.loc[
    macd_df.zero_crossover == "bearish_zero_cross"]

if not bull_sig.empty:
    fig_dist.add_trace(go.Scatter(
        x=bull_sig.index,
        y=bull_sig.macd_line,                 # put it where the MACD is
        mode="markers",
        marker=dict(symbol="triangle-up", color="green", size=12),
        name="Signal ↑",
        hovertemplate="%{x|%Y-%m-%d}<br>Bullish signal-line cross"
    ))
if not bear_sig.empty:
    fig_dist.add_trace(go.Scatter(
        x=bear_sig.index,
        y=bear_sig.macd_line,
        mode="markers",
        marker=dict(symbol="triangle-down", color="red", size=12),
        name="Signal ↓",
        hovertemplate="%{x|%Y-%m-%d}<br>Bearish signal-line cross"
    ))

# --- zero-line crosses (markers placed on y = 0) -------------------
if not bull_zero.empty:
    fig_dist.add_trace(go.Scatter(
        x=bull_zero.index,
        y=np.zeros(len(bull_zero)),           # stick it on the zero line
        mode="markers",
        marker=dict(symbol="circle", color="green", size=10,
                    line=dict(width=1, color="black")),
        name="Zero ↑",
        hovertemplate="%{x|%Y-%m-%d}<br>Bullish zero cross"
    ))
if not bear_zero.empty:
    fig_dist.add_trace(go.Scatter(
        x=bear_zero.index,
        y=np.zeros(len(bear_zero)),
        mode="markers",
        marker=dict(symbol="circle", color="red", size=10,
                    line=dict(width=1, color="black")),
        name="Zero ↓",
        hovertemplate="%{x|%Y-%m-%d}<br>Bearish zero cross"
    ))

st.plotly_chart(fig_dist)

