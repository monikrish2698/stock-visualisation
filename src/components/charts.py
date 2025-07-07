import plotly.graph_objects as go

def candlestick_chart(df, selected):
    data = [
        go.Candlestick(
        x = df.index,
        open = df["open"],
        high = df["high"],
        low = df["low"],
        close = df["close"],
        name = "Candlestick")
    ]
    if "5 day MA" in selected:
        data.append(
        go.Scatter(
        x = df.index,
        y = df.cumulative_5_day_ma,
        line=dict(color="orange", width=2),
        name = "5 day Moving Average")
    )
    if "20 day MA" in selected:
        data.append(
        go.Scatter(
        x = df.index,
        y = df.cumulative_20_day_ma,
        line=dict(color="blue", width=1),
        name = "20 day Moving Average")
    )
    if "50 day MA" in selected:
        data.append(
        go.Scatter(
        x = df.index,
        y = df.cumulative_50_day_ma,
        line=dict(color="green", width=1),
        name = "50 day Moving Average")
    )
    if "200 day MA" in selected:
        data.append(
        go.Scatter(
        x = df.index,
        y = df.cumulative_200_day_ma,
        line=dict(color="red", width=1),
        name = "200 day Moving Average")
    )
    
    return data
