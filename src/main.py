from stocks_data import get_stocks, explore_data
from returns import (
    get_daily_returns,
    print_daily_returns,
    print_avg_returns,
    print_risk,
    print_best_worst,
    print_cumulative,
)

# ── Step 1: Load data
print("⏳ Downloading stock data...")
stocks, close_prices = get_stocks()
print(f"✓ Loaded {len(stocks)} stocks, {len(close_prices)} trading days")

# ── Step 2: Explore
explore_data(close_prices)

# ── Step 3: Returns
daily_returns = get_daily_returns(close_prices)
print_daily_returns(daily_returns)
print_avg_returns(daily_returns)
print_risk(daily_returns)
print_best_worst(daily_returns)
print_cumulative(daily_returns)