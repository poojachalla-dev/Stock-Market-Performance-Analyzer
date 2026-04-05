import numpy as np

def get_daily_returns(close_prices):
    return close_prices.pct_change() * 100


def get_cumulative_returns(daily_returns):
    return (1 + daily_returns / 100).cumprod() * 100


def print_daily_returns(daily_returns):
    print("\n📊 Daily Returns (%)")
    print("=" * 60)
    print(daily_returns.head(10))


def print_avg_returns(daily_returns):
    print("\n📈 Average Daily Return (%) — per stock")
    print("=" * 60)
    avg_daily = daily_returns.mean().round(4).sort_values(ascending=False)
    for ticker, val in avg_daily.items():
        arrow = "📈" if val > 0 else "📉"
        print(f"  {arrow} {ticker:6}  {val:+.4f}% per day")


def print_risk(daily_returns):
    print("\n⚠️  Risk — Standard Deviation of Daily Returns")
    print("=" * 60)
    risk = daily_returns.std().round(4).sort_values(ascending=False)
    for ticker, val in risk.items():
        label = "🔴 High Risk" if val > 2 else "🟢 Lower Risk"
        print(f"  {ticker:6}  {val:.4f}%  {label}")


def print_best_worst(daily_returns):
    print("\n🚀 Best Single Day per Stock")
    print("=" * 60)
    print(daily_returns.max().round(2).sort_values(ascending=False))

    print("\n💥 Worst Single Day per Stock")
    print("=" * 60)
    print(daily_returns.min().round(2).sort_values())


def print_cumulative(daily_returns):
    print("\n💰 Cumulative Return — $100 invested at start of year")
    print("=" * 60)
    cumulative  = get_cumulative_returns(daily_returns)
    final_value = cumulative.iloc[-1].round(2).sort_values(ascending=False)
    for ticker, val in final_value.items():
        profit = val - 100
        arrow  = "📈" if profit > 0 else "📉"
        print(f"  {arrow} {ticker:6}  ${val:.2f}   ({profit:+.2f}%)")