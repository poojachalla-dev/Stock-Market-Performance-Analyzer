# dashboard.py — Streamlit dashboard for Stock Market Analyser
# Run with: streamlit run dashboard.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

# ── so we can import from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from stocks_data      import get_stocks
from returns    import get_daily_returns, get_cumulative_returns
from indicators import add_all_indicators

# ──────────────────────────────────────────────
# Page Config — must be first streamlit command
# ──────────────────────────────────────────────

st.set_page_config(
    page_title = "Stock Market Analyser",
    page_icon  = "📈",
    layout     = "wide"         # use full screen width
)

# ──────────────────────────────────────────────
# Load Data — cache it so it doesn't reload
# every time user clicks something
# ──────────────────────────────────────────────

@st.cache_data
def load_data():
    """Downloads and prepares all stock data."""
    stocks, close_prices = get_stocks()
    for ticker in stocks:
        stocks[ticker] = add_all_indicators(stocks[ticker])
    return stocks, close_prices

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────

st.title("📈 Stock Market Performance Analyser")
st.markdown("Real-time analysis of 10 major stocks using Python, Pandas & Plotly")
st.divider()

# ──────────────────────────────────────────────
# Load data with spinner
# ──────────────────────────────────────────────

with st.spinner("⏳ Downloading stock data..."):
    stocks, close_prices = load_data()

tickers = list(stocks.keys())
daily_returns = get_daily_returns(close_prices)
cumulative    = get_cumulative_returns(daily_returns)

st.success(f"✅ Loaded {len(stocks)} stocks successfully!")
st.divider()

# ──────────────────────────────────────────────
# Sidebar — controls
# ──────────────────────────────────────────────

st.sidebar.title("⚙️ Controls")
st.sidebar.markdown("Customise your analysis below")

# ticker selector for single stock charts
selected_ticker = st.sidebar.selectbox(
    "Select Stock for detailed view:",
    options = tickers,
    index   = 0
)

# multi select for comparison charts
selected_compare = st.sidebar.multiselect(
    "Select Stocks to compare:",
    options  = tickers,
    default  = tickers[:5]      # first 5 selected by default
)

st.sidebar.divider()
st.sidebar.markdown("Built with ❤️ using Python & Streamlit")

# ──────────────────────────────────────────────
# Row 1 — KPI Metrics (top numbers)
# ──────────────────────────────────────────────

st.subheader("📊 Key Metrics")

# calculate metrics for selected ticker
df_selected   = stocks[selected_ticker]
total_return  = ((df_selected["Close"].iloc[-1] / df_selected["Close"].iloc[0]) - 1) * 100
daily_vol     = daily_returns[selected_ticker].std()
current_price = df_selected["Close"].iloc[-1]
current_rsi   = df_selected["RSI"].iloc[-1]

# show 4 metric cards in a row
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label = f"💰 {selected_ticker} Price",
    value = f"${current_price:.2f}",
)

col2.metric(
    label = "📈 Total Return",
    value = f"{total_return:.2f}%",
    delta = f"{total_return:.2f}%"     # shows green/red arrow
)

col3.metric(
    label = "⚠️ Daily Volatility",
    value = f"{daily_vol:.2f}%",
)

col4.metric(
    label = "📉 RSI",
    value = f"{current_rsi:.1f}",
    delta = "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral"
)

st.divider()

# ──────────────────────────────────────────────
# Row 2 — Price History Chart
# ──────────────────────────────────────────────

st.subheader("📈 Price History")

fig_price = go.Figure()

for ticker in selected_compare:
    fig_price.add_trace(go.Scatter(
        x    = stocks[ticker].index,
        y    = stocks[ticker]["Close"],
        name = ticker,
        mode = "lines",
        line = dict(width=1.5)
    ))

fig_price.update_layout(
    title      = "Closing Price — Last 1 Year",
    xaxis_title = "Date",
    yaxis_title = "Price (USD)",
    hovermode  = "x unified",     # shows all stocks on hover
    height     = 450,
    template   = "plotly_dark",
)

st.plotly_chart(fig_price, use_container_width=True)

# ──────────────────────────────────────────────
# Row 3 — Cumulative Returns
# ──────────────────────────────────────────────

st.subheader("💰 Cumulative Returns — $100 Invested")

fig_cum = go.Figure()

for ticker in selected_compare:
    fig_cum.add_trace(go.Scatter(
        x    = cumulative.index,
        y    = cumulative[ticker],
        name = ticker,
        mode = "lines",
        line = dict(width=1.5)
    ))

# $100 baseline
fig_cum.add_hline(
    y           = 100,
    line_dash   = "dash",
    line_color  = "white",
    opacity     = 0.5,
    annotation_text = "Start ($100)"
)

fig_cum.update_layout(
    title       = "Growth of $100 Investment",
    xaxis_title = "Date",
    yaxis_title = "Portfolio Value ($)",
    hovermode   = "x unified",
    height      = 450,
    template    = "plotly_dark",
)

st.plotly_chart(fig_cum, use_container_width=True)

# ──────────────────────────────────────────────
# Row 4 — Moving Averages & RSI side by side
# ──────────────────────────────────────────────

st.subheader(f"📊 {selected_ticker} — Detailed Analysis")

col_left, col_right = st.columns(2)

# ── Moving Averages (left)
with col_left:
    fig_ma = go.Figure()

    fig_ma.add_trace(go.Scatter(
        x    = df_selected.index,
        y    = df_selected["Close"],
        name = "Close Price",
        line = dict(color="#00C9FF", width=1.5)
    ))

    fig_ma.add_trace(go.Scatter(
        x    = df_selected.index,
        y    = df_selected["SMA_20"],
        name = "SMA 20",
        line = dict(color="#FFD700", width=1.5, dash="dash")
    ))

    fig_ma.add_trace(go.Scatter(
        x    = df_selected.index,
        y    = df_selected["SMA_50"],
        name = "SMA 50",
        line = dict(color="#FF6B6B", width=1.5, dash="dash")
    ))

    fig_ma.update_layout(
        title    = "Price & Moving Averages",
        height   = 400,
        template = "plotly_dark",
        hovermode = "x unified"
    )

    st.plotly_chart(fig_ma, use_container_width=True)

# ── RSI (right)
with col_right:
    fig_rsi = go.Figure()

    fig_rsi.add_trace(go.Scatter(
        x    = df_selected.index,
        y    = df_selected["RSI"],
        name = "RSI",
        line = dict(color="#FF69B4", width=1.5),
        fill = "tozeroy",
        fillcolor = "rgba(255,105,180,0.1)"
    ))

    # overbought & oversold lines
    fig_rsi.add_hline(y=70, line_dash="dash",
                      line_color="red",   annotation_text="Overbought 70")
    fig_rsi.add_hline(y=30, line_dash="dash",
                      line_color="green", annotation_text="Oversold 30")

    fig_rsi.update_layout(
        title    = "RSI — Relative Strength Index",
        height   = 400,
        template = "plotly_dark",
        yaxis    = dict(range=[0, 100])
    )

    st.plotly_chart(fig_rsi, use_container_width=True)

# ──────────────────────────────────────────────
# Row 5 — Bollinger Bands
# ──────────────────────────────────────────────

st.subheader(f"📉 {selected_ticker} — Bollinger Bands")

fig_bb = go.Figure()

# shaded area between bands
fig_bb.add_trace(go.Scatter(
    x    = df_selected.index,
    y    = df_selected["BB_Upper"],
    name = "Upper Band",
    line = dict(color="rgba(255,107,107,0.3)", width=1),
))

fig_bb.add_trace(go.Scatter(
    x         = df_selected.index,
    y         = df_selected["BB_Lower"],
    name      = "Lower Band",
    line      = dict(color="rgba(107,255,107,0.3)", width=1),
    fill      = "tonexty",              # fills between upper and lower
    fillcolor = "rgba(0,201,255,0.05)"
))

fig_bb.add_trace(go.Scatter(
    x    = df_selected.index,
    y    = df_selected["Close"],
    name = "Close Price",
    line = dict(color="#00C9FF", width=1.5)
))

fig_bb.add_trace(go.Scatter(
    x    = df_selected.index,
    y    = df_selected["BB_Middle"],
    name = "SMA 20",
    line = dict(color="#FFD700", width=1, dash="dash")
))

fig_bb.update_layout(
    title     = "Bollinger Bands",
    height    = 450,
    template  = "plotly_dark",
    hovermode = "x unified"
)

st.plotly_chart(fig_bb, use_container_width=True)

# ──────────────────────────────────────────────
# Row 6 — Volatility & Correlation side by side
# ──────────────────────────────────────────────

st.subheader("⚠️ Risk Analysis")

col_v, col_c = st.columns(2)

# ── Volatility bar chart (left)
with col_v:
    volatility = daily_returns.std().sort_values(ascending=False)

    fig_vol = px.bar(
        x               = volatility.index,
        y               = volatility.values,
        color           = volatility.values,
        color_continuous_scale = "RdYlGn_r",
        labels          = {"x": "Stock", "y": "Volatility (%)"},
        title           = "Volatility Comparison"
    )

    fig_vol.update_layout(
        height       = 400,
        template     = "plotly_dark",
        showlegend   = False,
        coloraxis_showscale = False
    )

    st.plotly_chart(fig_vol, use_container_width=True)

# ── Correlation heatmap (right)
with col_c:
    corr = daily_returns.corr()

    fig_corr = px.imshow(
        corr,
        color_continuous_scale = "RdYlGn",
        zmin  = -1,
        zmax  = 1,
        title = "Correlation Heatmap",
        text_auto = ".2f"
    )

    fig_corr.update_layout(
        height   = 400,
        template = "plotly_dark"
    )

    st.plotly_chart(fig_corr, use_container_width=True)

# ──────────────────────────────────────────────
# Row 7 — Raw Data Table
# ──────────────────────────────────────────────

st.divider()
st.subheader("📋 Raw Data")

if st.checkbox("Show raw closing prices table"):
    st.dataframe(
        close_prices.tail(30).style.highlight_max(
            color="lightgreen"
        ).highlight_min(
            color="lightcoral"
        ),
        use_container_width=True
    )