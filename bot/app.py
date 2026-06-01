import streamlit as st
from binance.client import Client
from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import ta
import time

# =========================
# PREMIUM DARK GLASS UI
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #020617
    );
    color: white;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

div[data-testid="stVerticalBlock"] > div {
    border-radius: 18px;
}

.stButton button {
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 25px;
    font-size: 18px;
    font-weight: bold;
}

.stButton button:hover {
    background: linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );
    transform: scale(1.02);
}

h1, h2, h3 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

st.caption("⚡ Real-Time AI Powered Crypto Trading Dashboard")

# =========================
# Load Environment Variables
# =========================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# =========================
# Create Binance Client
# =========================

client = Client(API_KEY, API_SECRET)

# Binance Futures Testnet
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

# =========================
# Streamlit Page Config
# =========================

st.set_page_config(
    page_title="AI Trading Bot",
    layout="wide"
)
# Auto refresh every 5 sec
st_autorefresh = st.empty()

time.sleep(5)
# =========================
# Dashboard Title
# =========================

st.title("🚀 Binance Futures Trading Dashboard")

# =========================
# Live BTC Price
# =========================

ticker = client.get_symbol_ticker(symbol="BTCUSDT")
price = ticker["price"]

st.metric("BTCUSDT Live Price", f"${price}")

# =========================
# Success Message
# =========================

st.success("Binance API Connected Successfully ✅")

# =========================
# Fetch Historical Candles
# =========================

klines = client.futures_klines(
    symbol="BTCUSDT",
    interval="1m",
    limit=100
)

# =========================
# Convert to DataFrame
# =========================

df = pd.DataFrame(klines, columns=[
    "time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore"
])

# =========================
# Convert Data Types
# =========================

df["open"] = df["open"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)
df["close"] = df["close"].astype(float)

# =========================
# Technical Indicators
# =========================

# EMA 20
df["EMA20"] = ta.trend.ema_indicator(
    df["close"],
    window=20
)

# RSI
df["RSI"] = ta.momentum.rsi(
    df["close"],
    window=14
)

# =========================
# Create Candlestick Chart
# =========================

fig = go.Figure()

# Candlestick
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Candlestick"
    )
)

# EMA Line
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA20"],
        mode="lines",
        name="EMA 20"
    )
)

# =========================
# Chart Layout
# =========================

fig.update_layout(
    title="📈 BTCUSDT AI Trading Chart",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark",
    height=700,
    xaxis_rangeslider_visible=False
)

# =========================
# Display Chart
# =========================

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# AI Indicators Section
# =========================

st.subheader("📊 AI Trading Indicators")

latest_rsi = df["RSI"].iloc[-1]
latest_ema = df["EMA20"].iloc[-1]
current_price = df["close"].iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "RSI",
        round(latest_rsi, 2)
    )

with col2:
    st.metric(
        "EMA20",
        round(latest_ema, 2)
    )

# =========================
# AI Trading Signal
# =========================

st.subheader("🤖 AI Trading Signal")

if latest_rsi < 30:
    st.success("🟢 BUY SIGNAL → Market Oversold")

elif latest_rsi > 70:
    st.error("🔴 SELL SIGNAL → Market Overbought")

else:
    st.warning("🟡 HOLD SIGNAL → Wait for Better Entry")

# =========================
# Market Analysis
# =========================

st.subheader("📌 Market Analysis")

if current_price > latest_ema:
    st.info("📈 Price is ABOVE EMA20 → Bullish Trend")

else:
    st.info("📉 Price is BELOW EMA20 → Bearish Trend")
# =========================
# Leverage Control
# =========================

st.subheader("⚙️ Risk Management")

leverage = st.slider(
    "Select Leverage",
    min_value=1,
    max_value=20,
    value=5
)

# Set leverage
client.futures_change_leverage(
    symbol="BTCUSDT",
    leverage=leverage
)

st.success(f"Leverage Set to {leverage}x")
# =========================
# Manual Trading Panel
# =========================

st.subheader("⚡ Manual Trading Panel")

trade_side = st.selectbox(
    "Select Side",
    ["BUY", "SELL"]
)

quantity = st.number_input(
    "Enter Quantity",
    min_value=0.001,
    value=0.001,
    step=0.001
)
# =========================
# TP / SL Inputs
# =========================

take_profit = st.number_input(
    "Take Profit Price",
    value=72000.0
)

stop_loss = st.number_input(
    "Stop Loss Price",
    value=70000.0
)
if st.button("🚀 Execute Trade"):

    try:

        # =========================
        # Main Market Order
        # =========================

        order = client.futures_create_order(
            symbol="BTCUSDT",
            side=trade_side,
            type="MARKET",
            quantity=quantity
        )

        # =========================
        # TP / SL Orders
        # =========================

        if trade_side == "BUY":

            # Take Profit
            client.futures_create_order(
                symbol="BTCUSDT",
                side="SELL",
                type="TAKE_PROFIT_MARKET",
                stopPrice=take_profit,
                closePosition=True
            )

            # Stop Loss
            client.futures_create_order(
                symbol="BTCUSDT",
                side="SELL",
                type="STOP_MARKET",
                stopPrice=stop_loss,
                closePosition=True
            )

        else:

            # Take Profit
            client.futures_create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="TAKE_PROFIT_MARKET",
                stopPrice=take_profit,
                closePosition=True
            )

            # Stop Loss
            client.futures_create_order(
                symbol="BTCUSDT",
                side="BUY",
                type="STOP_MARKET",
                stopPrice=stop_loss,
                closePosition=True
            )

        st.success("✅ Trade Executed Successfully")
        st.success("🎯 TP/SL Orders Added Successfully")

        st.json(order)

    except Exception as e:

        st.error(f"❌ Error: {str(e)}")

# =========================
# Trade History
# =========================

st.subheader("📜 Recent Trade History")

try:

    trades = client.futures_account_trades(symbol="BTCUSDT")

    if len(trades) > 0:

        trade_data = []

        for trade in trades[-10:]:

            trade_data.append({
                "Price": trade["price"],
                "Qty": trade["qty"],
                "Side": trade["side"],
                "Realized PnL": trade["realizedPnl"],
                "Time": trade["time"]
            })

        trades_df = pd.DataFrame(trade_data)

        st.dataframe(
            trades_df,
            use_container_width=True
        )

    else:

        st.warning("No trades found.")

except Exception as e:

    st.error(f"Trade History Error: {str(e)}")