import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="AI Binance Futures Trading Dashboard",
    page_icon="🚀",
    layout="wide"
)

# =======================
# PREMIUM DARK UI
# =======================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(90deg,#020617,#0f172a,#020617);
    color: white;
}

h1,h2,h3 {
    color:white !important;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    padding:20px;
    border-radius:20px;
}

.stButton button {
    background: linear-gradient(90deg,#06b6d4,#3b82f6);
    color:white;
    border:none;
    border-radius:12px;
    padding:12px 30px;
    font-weight:bold;
}

.block-container {
    padding-top:2rem;
}
</style>
""", unsafe_allow_html=True)

# =======================
# FAKE LIVE DATA
# =======================

btc_price = 71200
rsi = 25.54
ema20 = 71200.53

signal = "BUY SIGNAL → Market Oversold"

# =======================
# HEADER
# =======================

st.markdown("### ⚡ Real-Time AI Powered Crypto Trading Dashboard")

st.title("🚀 Binance Futures Trading Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("BTCUSDT", f"${btc_price}")

with col2:
    st.metric("RSI", rsi)

with col3:
    st.metric("EMA20", ema20)

st.success("Binance API Connected Successfully ✅")

# =======================
# CHART
# =======================

prices = np.random.normal(71200, 120, 100)

fig = go.Figure()

fig.add_trace(go.Scatter(
    y=prices,
    mode='lines',
    name='BTC Price'
))

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# =======================
# AI SIGNALS
# =======================

st.header("🧠 AI Trading Signal")

st.success(signal)

# =======================
# MARKET ANALYSIS
# =======================

st.header("📌 Market Analysis")

if btc_price > ema20:
    st.info("Price is ABOVE EMA20 → Bullish Trend")
else:
    st.warning("Price is BELOW EMA20 → Bearish Trend")

# =======================
# RISK MANAGEMENT
# =======================

st.header("⚙️ Risk Management")

leverage = st.slider("Select Leverage", 1, 20, 5)

st.success(f"Leverage Set to {leverage}x")

# =======================
# MANUAL TRADING PANEL
# =======================

st.header("⚡ Manual Trading Panel")

side = st.selectbox("Select Side", ["BUY", "SELL"])

qty = st.number_input("Enter Quantity", value=0.001)

tp = st.number_input("Take Profit Price", value=72000.0)

sl = st.number_input("Stop Loss Price", value=70000.0)

if st.button("🚀 Execute Trade"):
    st.success(f"{side} Trade Executed Successfully")

# =======================
# TRADE HISTORY
# =======================

st.header("📜 Recent Trade History")

trade_data = pd.DataFrame({
    "Price":[71451.70,71215.10],
    "Qty":[0.0010,0.0010],
    "Side":["BUY","BUY"],
    "PnL":[0,0],
    "Time":[datetime.now(),datetime.now()]
})

st.dataframe(trade_data, use_container_width=True)

# =======================
# FOOTER
# =======================

st.markdown("---")
st.markdown("### 🚀 Developed by Rahul Aryan")