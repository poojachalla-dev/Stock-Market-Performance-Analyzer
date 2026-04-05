import pandas as pd
import numpy as np
import yfinance as yf

# ── Step 1: Downloading the Data from yfinance
# 10 major stocks across different sectors
tickers = ["MSFT", "AAPL", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "UNH"]

# Download all together
df = yf.download(tickers, period="1y", auto_adjust=True)

# Empty dictionary to store each stock separately
stocks = {}

# Loop through each ticker and extract its data
for ticker in tickers:
    stocks[ticker] = pd.DataFrame({
        "Open"  : df["Open"][ticker],
        "High"  : df["High"][ticker],
        "Low"   : df["Low"][ticker],
        "Close" : df["Close"][ticker],
        "Volume": df["Volume"][ticker],
    })
    print(f"✓ {ticker} — {len(stocks[ticker])} rows loaded")

# ── Show close prices for all stocks in one clean table
print("\n📊 Closing Prices — All Stocks")
print("=" * 60)

close_prices = pd.DataFrame({
    ticker: stocks[ticker]["Close"]
    for ticker in tickers
})

print(close_prices)

# ── Step 2: Exploring the data
print("\n📊 Summary Statistics — Closing Prices")
print("=" * 60)

# describe() gives you count, mean, min, max, std in one shot
print(close_prices.describe().round(2))

print("\n💰 Average Closing Price (highest to lowest)")
print("=" * 60)

avg_prices = close_prices.mean().sort_values(ascending=False).round(2)
print(avg_prices)

print("\n📈 Total Growth This Year (%)")
print("=" * 60)

# First price of the year vs last price
first_price = close_prices.iloc[0]   # first row  = oldest date
last_price  = close_prices.iloc[-1]  # last row   = most recent date

growth = ((last_price - first_price) / first_price * 100).round(2)
growth = growth.sort_values(ascending=False)

for ticker, pct in growth.items():
    arrow = "📈" if pct > 0 else "📉"
    print(f"  {arrow} {ticker:6} {pct:+.2f}%")

print("\n🔍 Missing Values Check")
print("=" * 60)

missing = close_prices.isnull().sum()
print(missing)

# ── Step 3: Calculating Returns
print("\n📊 Daily Returns (%)")
print("=" * 60)

# pct_change() does the formula above automatically for every row
daily_returns = close_prices.pct_change() * 100

print(daily_returns.head(10))

# Average Daily Return
print("\n📈 Average Daily Return (%) — per stock")
print("=" * 60)

avg_daily = daily_returns.mean().round(4).sort_values(ascending=False)

for ticker, val in avg_daily.items():
    arrow = "📈" if val > 0 else "📉"
    print(f"  {arrow} {ticker:6}  {val:+.4f}% per day")

#Risk(Standard Deviation)
print("\n⚠️  Risk — Standard Deviation of Daily Returns")
print("=" * 60)

risk = daily_returns.std().round(4).sort_values(ascending=False)

for ticker, val in risk.items():
    print(f"  {ticker:6}  {val:.4f}%  {'🔴 High Risk' if val > 2 else '🟢 Lower Risk'}")


#Best and Worst Single Days
print("\n🚀 Best Single Day per Stock")
print("=" * 60)
print(daily_returns.max().round(2).sort_values(ascending=False))

print("\n💥 Worst Single Day per Stock")
print("=" * 60)
print(daily_returns.min().round(2).sort_values())

#Cummulative
print("\n💰 Cumulative Return — $100 invested at start of year")
print("=" * 60)

# (1 + return/100) compounds day by day
cumulative = (1 + daily_returns / 100).cumprod() * 100

# Show final value only
final_value = cumulative.iloc[-1].round(2).sort_values(ascending=False)

for ticker, val in final_value.items():
    profit = val - 100
    arrow  = "📈" if profit > 0 else "📉"
    print(f"  {arrow} {ticker:6}  ${val:.2f}   ({profit:+.2f}%)")

