import pandas as pd
import yfinance as yf

tickers = ["MSFT", "AAPL", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "UNH"]

def get_stocks():
    data = yf.download(tickers, period="1y", auto_adjust=True, progress=False)

    stocks = {}
    for ticker in tickers:
        stocks[ticker] = pd.DataFrame({
            "Open"  : data["Open"][ticker],
            "High"  : data["High"][ticker],
            "Low"   : data["Low"][ticker],
            "Close" : data["Close"][ticker],
            "Volume": data["Volume"][ticker],
        })

    close_prices = pd.DataFrame({
        ticker: stocks[ticker]["Close"]
        for ticker in tickers
    })

    return stocks, close_prices


def explore_data(close_prices):
    print("\n📊 Summary Statistics — Closing Prices")
    print("=" * 60)
    print(close_prices.describe().round(2))

    print("\n💰 Average Closing Price (highest to lowest)")
    print("=" * 60)
    avg_prices = close_prices.mean().sort_values(ascending=False).round(2)
    print(avg_prices)

    print("\n📈 Total Growth This Year (%)")
    print("=" * 60)
    first_price = close_prices.iloc[0]
    last_price  = close_prices.iloc[-1]
    growth = ((last_price - first_price) / first_price * 100).round(2)
    growth = growth.sort_values(ascending=False)
    for ticker, pct in growth.items():
        arrow = "📈" if pct > 0 else "📉"
        print(f"  {arrow} {ticker:6} {pct:+.2f}%")

    print("\n🔍 Missing Values Check")
    print("=" * 60)
    print(close_prices.isnull().sum())