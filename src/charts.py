    # charts.py — all matplotlib visualisations
# Each function creates and saves one chart

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
import os

# ── Create plots folder if it doesn't exist
os.makedirs("plots", exist_ok=True)

# ── Global chart style — dark theme looks great on GitHub
plt.style.use("dark_background")

COLORS = ["#00C9FF", "#FF6B6B", "#6BFF6B", "#FFD700",
          "#FF69B4", "#FF8C00", "#00FA9A", "#BA55D3",
          "#00BFFF", "#FF4500"]


# ──────────────────────────────────────────────
# Chart 1 — Stock Price History
# ──────────────────────────────────────────────

def plot_price_history(stocks, tickers):
    """
    Line chart showing closing price of all stocks over the year.
    Each stock gets its own colour.
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    for i, ticker in enumerate(tickers):
        ax.plot(
            stocks[ticker].index,
            stocks[ticker]["Close"],
            label=ticker,
            color=COLORS[i],
            linewidth=1.5
        )

    ax.set_title("📈 Stock Price History — Last 1 Year",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Price (USD)", fontsize=12)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig("plots/01_price_history.png", dpi=150)
    plt.close()
    print("  ✓ Saved: plots/01_price_history.png")


# ──────────────────────────────────────────────
# Chart 2 — Cumulative Returns
# ──────────────────────────────────────────────

def plot_cumulative_returns(close_prices, tickers):
    """
    Shows how $100 invested in each stock grows over the year.
    Best way to compare performance across stocks.
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # calculate daily returns then compound them
    daily_returns = close_prices.pct_change()
    cumulative    = (1 + daily_returns).cumprod() * 100

    for i, ticker in enumerate(tickers):
        ax.plot(
            cumulative.index,
            cumulative[ticker],
            label=ticker,
            color=COLORS[i],
            linewidth=1.5
        )

    # $100 baseline
    ax.axhline(y=100, color="white", linewidth=0.8,
               linestyle="--", alpha=0.5, label="Start ($100)")

    ax.set_title("💰 Cumulative Returns — $100 Invested",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Portfolio Value ($)", fontsize=12)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig("plots/02_cumulative_returns.png", dpi=150)
    plt.close()
    print("  ✓ Saved: plots/02_cumulative_returns.png")


# ──────────────────────────────────────────────
# Chart 3 — Moving Averages (one stock)
# ──────────────────────────────────────────────

def plot_moving_averages(stocks, ticker="AAPL"):
    """
    Shows Close price + SMA20 + SMA50 for one stock.
    Helps visualise the trend clearly.
    """
    df  = stocks[ticker]
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df.index, df["Close"],
            label="Close Price", color="#00C9FF",
            linewidth=1.2, alpha=0.8)

    ax.plot(df.index, df["SMA_20"],
            label="SMA 20 days", color="#FFD700",
            linewidth=1.5, linestyle="--")

    ax.plot(df.index, df["SMA_50"],
            label="SMA 50 days", color="#FF6B6B",
            linewidth=1.5, linestyle="--")

    ax.set_title(f"📊 {ticker} — Price & Moving Averages",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Price (USD)", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(f"plots/03_moving_averages_{ticker}.png", dpi=150)
    plt.close()
    print(f"  ✓ Saved: plots/03_moving_averages_{ticker}.png")


# ──────────────────────────────────────────────
# Chart 4 — RSI Chart (one stock)
# ──────────────────────────────────────────────

def plot_rsi(stocks, ticker="AAPL"):
    """
    Two-panel chart:
    Top    → closing price
    Bottom → RSI with overbought/oversold zones
    """
    df  = stocks[ticker]

    # two panels stacked vertically
    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(14, 8),
        gridspec_kw={"height_ratios": [2, 1]},  # top panel 2x taller
        sharex=True                               # same x-axis dates
    )

    # ── Top panel: price
    ax1.plot(df.index, df["Close"],
             color="#00C9FF", linewidth=1.5, label="Close")
    ax1.set_title(f"📉 {ticker} — Price & RSI",
                  fontsize=16, fontweight="bold", pad=15)
    ax1.set_ylabel("Price (USD)", fontsize=11)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.2)

    # ── Bottom panel: RSI
    ax2.plot(df.index, df["RSI"],
             color="#FF69B4", linewidth=1.2, label="RSI")

    # overbought zone (red) and oversold zone (green)
    ax2.axhline(70, color="#FF6B6B", linewidth=1,
                linestyle="--", label="Overbought (70)")
    ax2.axhline(30, color="#6BFF6B", linewidth=1,
                linestyle="--", label="Oversold (30)")

    ax2.fill_between(df.index, 70, 100,
                     alpha=0.1, color="#FF6B6B")
    ax2.fill_between(df.index, 0, 30,
                     alpha=0.1, color="#6BFF6B")

    ax2.set_ylim(0, 100)
    ax2.set_ylabel("RSI", fontsize=11)
    ax2.set_xlabel("Date", fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(f"plots/04_rsi_{ticker}.png", dpi=150)
    plt.close()
    print(f"  ✓ Saved: plots/04_rsi_{ticker}.png")


# ──────────────────────────────────────────────
# Chart 5 — Bollinger Bands (one stock)
# ──────────────────────────────────────────────

def plot_bollinger_bands(stocks, ticker="AAPL"):
    """
    Shows price inside Bollinger Bands.
    Shaded area between upper and lower bands.
    """
    df  = stocks[ticker]
    fig, ax = plt.subplots(figsize=(14, 6))

    # price line
    ax.plot(df.index, df["Close"],
            color="#00C9FF", linewidth=1.2,
            label="Close Price", zorder=3)

    # middle band (SMA 20)
    ax.plot(df.index, df["BB_Middle"],
            color="#FFD700", linewidth=1,
            linestyle="--", label="SMA 20 (Middle)")

    # upper and lower bands
    ax.plot(df.index, df["BB_Upper"],
            color="#FF6B6B", linewidth=0.8,
            linestyle="--", label="Upper Band")

    ax.plot(df.index, df["BB_Lower"],
            color="#6BFF6B", linewidth=0.8,
            linestyle="--", label="Lower Band")

    # shaded area between bands
    ax.fill_between(df.index,
                    df["BB_Upper"], df["BB_Lower"],
                    alpha=0.08, color="#00C9FF")

    ax.set_title(f"📊 {ticker} — Bollinger Bands",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Price (USD)", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(f"plots/05_bollinger_{ticker}.png", dpi=150)
    plt.close()
    print(f"  ✓ Saved: plots/05_bollinger_{ticker}.png")


# ──────────────────────────────────────────────
# Chart 6 — Volatility (Risk) Comparison
# ──────────────────────────────────────────────

def plot_volatility(close_prices, tickers):
    """
    Bar chart comparing how risky/volatile each stock is.
    Higher bar = more volatile = riskier.
    """
    daily_returns = close_prices.pct_change() * 100
    volatility    = daily_returns.std().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_colors = [
        "#FF6B6B" if v > 2.5 else
        "#FFD700" if v > 1.5 else
        "#6BFF6B"
        for v in volatility.values
    ]

    bars = ax.bar(volatility.index, volatility.values,
                  color=bar_colors, width=0.5, edgecolor="white",
                  linewidth=0.5)

    # add value labels on top of each bar
    for bar, val in zip(bars, volatility.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"{val:.2f}%",
            ha="center", va="bottom",
            fontsize=10, fontweight="bold"
        )

    ax.set_title("⚠️  Volatility Comparison — Daily Return Std Dev",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Stock", fontsize=12)
    ax.set_ylabel("Volatility (Std Dev %)", fontsize=12)
    ax.grid(True, alpha=0.2, axis="y")

    # legend
    from matplotlib.patches import Patch
    legend = [
        Patch(color="#FF6B6B", label="🔴 High Risk  (>2.5%)"),
        Patch(color="#FFD700", label="🟡 Medium Risk (1.5–2.5%)"),
        Patch(color="#6BFF6B", label="🟢 Lower Risk  (<1.5%)"),
    ]
    ax.legend(handles=legend, fontsize=9)

    plt.tight_layout()
    plt.savefig("plots/06_volatility.png", dpi=150)
    plt.close()
    print("  ✓ Saved: plots/06_volatility.png")


# ──────────────────────────────────────────────
# Chart 7 — Correlation Heatmap
# ──────────────────────────────────────────────

def plot_correlation(close_prices):
    """
    Heatmap showing how closely stocks move together.
    1.0 = move perfectly together
    0.0 = no relation
    -1  = move in opposite directions
    """
    daily_returns = close_prices.pct_change()
    corr          = daily_returns.corr()

    fig, ax = plt.subplots(figsize=(10, 8))

    # draw heatmap manually with imshow
    im = ax.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1)

    # add ticker labels
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=10)
    ax.set_yticklabels(corr.columns, fontsize=10)

    # add correlation values inside each cell
    for i in range(len(corr)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}",
                    ha="center", va="center",
                    fontsize=9, fontweight="bold",
                    color="black")

    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax.set_title("🔗 Stock Correlation Heatmap",
                 fontsize=16, fontweight="bold", pad=15)

    plt.tight_layout()
    plt.savefig("plots/07_correlation.png", dpi=150)
    plt.close()
    print("  ✓ Saved: plots/07_correlation.png")