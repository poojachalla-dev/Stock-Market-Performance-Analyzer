# main.py — runs the full Stock Market Analyser

import sys
import os
sys.path.append(os.path.dirname(__file__))

from stocks_data       import get_stocks, explore_data
from returns    import (
    get_daily_returns,
    print_daily_returns,
    print_avg_returns,
    print_risk,
    print_best_worst,
    print_cumulative,
)
from indicators import add_all_indicators, print_latest_indicators
from charts     import (
    plot_price_history,
    plot_cumulative_returns,
    plot_moving_averages,
    plot_rsi,
    plot_bollinger_bands,
    plot_volatility,
    plot_correlation,
)

tickers = ["MSFT", "AAPL", "GOOGL", "AMZN", "META",
           "TSLA", "NVDA", "JPM", "V", "UNH"]

# ── Step 1 & 2: Load & Explore
print("⏳ Downloading stock data...")
stocks, close_prices = get_stocks()
print(f"✓ Loaded {len(stocks)} stocks\n")
explore_data(close_prices)

# ── Step 3: Returns
daily_returns = get_daily_returns(close_prices)
print_daily_returns(daily_returns)
print_avg_returns(daily_returns)
print_risk(daily_returns)
print_best_worst(daily_returns)
print_cumulative(daily_returns)

# ── Step 4: Indicators
print("\n⏳ Calculating indicators...")
for ticker in tickers:
    stocks[ticker] = add_all_indicators(stocks[ticker])
print("✓ Done!\n")
print_latest_indicators(stocks)

# ── Step 5: Charts
print("\n📊 Generating charts...")
plot_price_history(stocks, tickers)
plot_cumulative_returns(close_prices, tickers)
plot_moving_averages(stocks, ticker="AAPL")
plot_rsi(stocks, ticker="AAPL")
plot_bollinger_bands(stocks, ticker="AAPL")
plot_volatility(close_prices, tickers)
plot_correlation(close_prices)
print("✓ All charts saved to plots/\n")

print("=" * 60)
print("  ✅ Analysis complete!")
print("  📁 Check the plots/ folder for all charts")
print("=" * 60)