# 📈 Stock Market Performance Analyzer

A Python project that downloads, analyses, and visualises
real stock market data using NumPy, Pandas, and Matplotlib.

## 🔍 What it does
- Downloads 1 year of real stock data (10 major stocks)
- Calculates daily & cumulative returns
- Measures risk using standard deviation
- Adds technical indicators (SMA, EMA, RSI, Bollinger Bands)
- Generates 7 professional charts

## 📊 Charts Generated
| Chart | Description |
|---|---|
| Price History | Closing prices for all 10 stocks |
| Cumulative Returns | How $100 grows over the year |
| Moving Averages | SMA 20 & SMA 50 trend lines |
| RSI | Overbought & oversold signals |
| Bollinger Bands | Volatility bands around price |
| Volatility | Risk comparison across stocks |
| Correlation | How stocks move together |

## 🛠️ Tech Stack
- **Python 3.x**
- **Pandas** — data manipulation
- **NumPy** — numerical calculations
- **Matplotlib** — charts & visualisations
- **yfinance** — real stock data

## 🚀 How to Run
```bash
# 1. Clone the repo
git clone https://github.com/yourusername/Stock-Market-Performance-Analyzer.git

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the analyser
cd src
python main.py
```

## 📁 Project Structure
```
Stock-Market-Performance-Analyzer/
│
├── src/
│   ├── data.py          # Download & explore stock data
│   ├── returns.py       # Return & risk calculations
│   ├── indicators.py    # Technical indicators
│   ├── charts.py        # Matplotlib visualisations
│   └── main.py          # Main entry point
│
├── plots/               # Generated charts saved here
├── requirements.txt
└── README.md
```

## 📸 Sample Charts
*(Add your chart screenshots here after running)*

## 👤 Author
Your Name — [GitHub](https://github.com/yourusername)
