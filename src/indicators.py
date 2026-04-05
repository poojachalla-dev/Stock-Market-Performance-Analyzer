# indicators.py — moving averages & technical indicators

import pandas as pd
import numpy as np


def add_moving_averages(df):
    """
    Adds SMA and EMA columns to a single stock's DataFrame.
    df must have a 'Close' column.
    """

    # ── Simple Moving Average (SMA)
    # plain average of last N closing prices
    df["SMA_20"]  = df["Close"].rolling(window=20).mean()
    df["SMA_50"]  = df["Close"].rolling(window=50).mean()

    # ── Exponential Moving Average (EMA)
    # gives MORE weight to recent prices
    df["EMA_20"]  = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA_50"]  = df["Close"].ewm(span=50, adjust=False).mean()

    return df


def add_rsi(df, period=14):
    """
    RSI — Relative Strength Index.
    Measures if a stock is overbought (>70) or oversold (<30).
    """
    delta = df["Close"].diff()           # daily price change

    gain  = delta.clip(lower=0)          # keep only positive days
    loss  = -delta.clip(upper=0)         # keep only negative days

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs  = avg_gain / avg_loss            # ratio of gains to losses
    df["RSI"] = 100 - (100 / (1 + rs))

    return df


def add_bollinger_bands(df, window=20):
    """
    Bollinger Bands — shows how volatile a stock is.
    Upper band = SMA + 2 standard deviations
    Lower band = SMA - 2 standard deviations
    """
    sma = df["Close"].rolling(window).mean()
    std = df["Close"].rolling(window).std()

    df["BB_Middle"] = sma
    df["BB_Upper"]  = sma + 2 * std
    df["BB_Lower"]  = sma - 2 * std

    return df


def add_all_indicators(df):
    """Adds all indicators to a stock DataFrame."""
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_bollinger_bands(df)
    return df


def print_latest_indicators(stocks):
    """Prints the latest indicator values for all stocks."""

    print("\n📊 Latest Indicator Values")
    print("=" * 70)
    print(f"  {'Ticker':6}  {'Close':>8}  {'SMA20':>8}  {'SMA50':>8}  {'RSI':>6}  Signal")
    print("-" * 70)

    for ticker, df in stocks.items():
        latest = df.iloc[-1]            # most recent row

        close = latest["Close"]
        sma20 = latest["SMA_20"]
        sma50 = latest["SMA_50"]
        rsi   = latest["RSI"]

        # ── Trading signal logic
        if rsi > 70:
            signal = "🔴 Overbought"
        elif rsi < 30:
            signal = "🟢 Oversold"
        elif close > sma20 > sma50:
            signal = "📈 Uptrend"
        elif close < sma20 < sma50:
            signal = "📉 Downtrend"
        else:
            signal = "⚪ Neutral"

        print(f"  {ticker:6}  {close:>8.2f}  {sma20:>8.2f}  {sma50:>8.2f}  {rsi:>6.1f}  {signal}")