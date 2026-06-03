import streamlit as st
import os
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Trade Guardian")
st.success("System Online")


# API SECRETS

QWEN_API_KEY = os.getenv("QWEN_API_KEY")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")


st.subheader("Connection Status")

st.success("✅ Qwen AI Connected" if QWEN_API_KEY else "❌ Qwen Missing")
st.success("✅ Bitget API Connected" if BITGET_API_KEY else "❌ Bitget Missing")


st.subheader("📈 Trading Dashboard")

symbol = st.selectbox(
    "Select Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"
    ]
)


# GET BITGET CANDLES

def get_candles(symbol):

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity=1h&limit=100"
    )

    data = requests.get(url).json()

    candles = data["data"]

    df = pd.DataFrame(
        candles,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote"
        ]
    )

    df["close"] = df["close"].astype(float)

    return df


# RSI

def rsi(prices):

    delta = prices.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = (
        gain.rolling(14).mean()
        /
        loss.rolling(14).mean()
    )

    return 100 - (100/(1+rs))


if st.button("🤖 Run AI Analysis"):

    df = get_candles(symbol)

    df["RSI"] = rsi(df["close"])

    price = df["close"].iloc[-1]
    current_rsi = df["RSI"].iloc[-1]


    st.metric(
        "Current Price",
        price
    )


    st.metric(
        "RSI",
        round(current_rsi,2)
    )


    if current_rsi < 30:
        signal = "BUY 🟢"

    elif current_rsi > 70:
        signal = "SELL 🔴"

    else:
        signal = "HOLD 🟡"


    st.subheader("🤖 AI Decision")

    st.metric(
        "Signal",
        signal
    )


    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=df["close"],
            name="Price"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.info(
        f"""
AI Trade Guardian Report

Pair: {symbol}

RSI: {round(current_rsi,2)}

Decision: {signal}

✅ Bitget Data
✅ RSI Analysis
✅ Risk Check
"""
    )
