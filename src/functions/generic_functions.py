from pyiceberg.catalog import load_catalog

import streamlit as st
import pandas as pd

catalog = load_catalog("prod")

@st.cache_data(ttl = 3600, show_spinner = False)
def get_all_tickers() -> pd.DataFrame:

    all_tickers = (
        catalog.load_table("monk_data_warehouse.dim_tickers")
        .scan(
            row_filter = "market = 'stocks'", 
            selected_fields = ["ticker", "name"])
        .to_duckdb(table_name = "all_tickers"))
    
    return all_tickers.execute("""select * from all_tickers""").df()

@st.cache_data(ttl = 3600, show_spinner = False)
def get_daily_prices_for_a_ticker(ticker: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    daily_prices = (
        catalog.load_table("monk_data_warehouse.fct_daily_stock_prices")
        .scan(
            row_filter = (
                f"ticker == '{ticker}' "
                f"and date >= '{start.strftime('%Y-%m-%d')}'"
                f"and date <= '{end.strftime('%Y-%m-%d')}'"),
            selected_fields = ["date","aggregates"])
        .to_duckdb(table_name = "daily_prices"))
    
    ticker_ema = (
        catalog.load_table("monishk37608.dm_simple_moving_averages")
        .scan(
            row_filter = (
                f"ticker == '{ticker}' "
                f"and date >= '{start.strftime('%Y-%m-%d')}' "
                f"and date <= '{end.strftime('%Y-%m-%d')}'"
            ),
            selected_fields = ["date", "cumulative_5_day_ma", "cumulative_20_day_ma", "cumulative_50_day_ma", "cumulative_200_day_ma"])
        .to_duckdb(table_name = "ticker_ema"))
    exec_daily_prices = daily_prices.execute("select * from daily_prices")
    exec_ticker_ema = ticker_ema.execute("select * from ticker_ema")

    prices_df =  exec_daily_prices.df()
    ema_df = exec_ticker_ema.df()
    merged_df = pd.merge(prices_df, ema_df, on = "date")
    return merged_df

@st.cache_data(ttl = 3600, show_spinner = False)
def get_macd_for_a_ticker(ticker: str) -> pd.DataFrame:
    macd = (
        catalog.load_table("monishk37608.dm_macd_crossover")
        .scan(
            row_filter = (
                f"ticker == '{ticker}'"
                f"and signal_line is not null"
                
            ),
            selected_fields = ["date", "macd_line", "signal_line", "signal_line_crossover", "zero_crossover"])
        .to_duckdb(table_name = "macd")
    )

    exec_macd = macd.execute("select date, macd_line, signal_line, macd_line - signal_line as histogram, signal_line_crossover, zero_crossover from macd")

    return exec_macd.df()


@st.cache_data(ttl = 3600, show_spinner = False)
def get_all_macd_tickers() -> pd.DataFrame:
    all_tickers = (
        catalog.load_table("monishk37608.dm_macd_crossover")
        .scan(
            row_filter = "signal_line is not null", 
            selected_fields = ["ticker"])
        .to_duckdb(table_name = "macd_tickers"))
    
    return all_tickers.execute("""select distinct ticker from macd_tickers""").df()



@st.cache_data(ttl = 3600, show_spinner = False)
def get_volatility_tickers() -> pd.DataFrame:
    volatility_tickers = (
        catalog.load_table("monishk37608.dm_annualised_volatility")
        .scan(
            row_filter = (
                f"date >= '2025-04-14' "
                f"and annualised_7d_volatility is not null "
                f"and annualised_30d_volatility is not null "
            ),
            selected_fields = ["ticker", "annualised_7d_volatility", "annualised_30d_volatility", "date"])
        .to_duckdb(table_name = "volatility_tickers"))
    
    return volatility_tickers.execute("select ticker, annualised_7d_volatility, annualised_30d_volatility, date from volatility_tickers").df()

@st.cache_data(ttl = 3600, show_spinner = False)
def get_ticker_details() -> pd.DataFrame:
    ticker_details = (
        catalog.load_table("monk_data_warehouse.dim_tickers")
        .scan(
            row_filter = (
                "market = 'stocks' "
                "and market_cap is not null "
            ),
            selected_fields = ["ticker", "name", "market", "sic_description", "sic_code", "market_cap"])
        .to_duckdb(table_name = "ticker_details"))
    
    return ticker_details.execute("""select 
    *, 
    case
    when market_cap >= 200000000000 then 'Mega Cap'
    when market_cap >= 10000000000 then 'Large Cap'
    when market_cap >= 2000000000 then 'Mid Cap'
    else 'Small Cap'
    end as market_cap_size
    from ticker_details""").df()

@st.cache_data(ttl = 3600, show_spinner = False)
def get_ema_for_a_ticker(ticker: str) -> pd.DataFrame:
    ema = (
        catalog.load_table("monishk37608.dm_exponential_moving_averages")
        .scan(
            row_filter = (
                f"ticker == '{ticker}'"
            ),
            selected_fields = ["date", "ema_12_day", "ema_26_day"])
        .to_duckdb(table_name = "ema")
    )

    min_date = ema.execute("select min(date) as date from ema").df().iloc[0]["date"]
    print("min_date", min_date)
    daily_prices = (
        catalog.load_table("monk_data_warehouse.fct_daily_stock_prices")
        .scan(
            row_filter = (
                f"ticker == '{ticker}' "
                f"and date >= '{min_date.strftime('%Y-%m-%d')}'"),
            selected_fields = ["date","aggregates"])
        .to_duckdb(table_name = "daily_prices"))

    exec_ema = ema.execute("select * from ema")

    exec_daily_prices = daily_prices.execute("select * from daily_prices")

    prices_df =  exec_daily_prices.df()
    ema_df = exec_ema.df()
    merged_df = pd.merge(prices_df, ema_df, on = "date")
    return merged_df


@st.cache_data(ttl = 3600, show_spinner = False)
def get_sentiment_overview(ticker: str) -> pd.DataFrame:
    sentiment = (
        
    )