import streamlit as st
import os
import requests
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from openai import OpenAI


st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Trade Guardian")
st.success("System Online")

st_autorefresh(
    interval=60000,
    key="refresh"
)


# =====================
# SECRETS
# =====================

QWEN_API_KEY = os.getenv("QWEN_API_KEY")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)


# =====================
# STATUS
# =====================

st.subheader("Connection Status")

st.success(
    "✅ Qwen AI Connected"
    if QWEN_API_KEY
    else "❌ Qwen Missing"
)

st.success(
    "✅ Bitget API Connected"
    if BITGET_API_KEY
    else "❌ Bitget Missing"
)


# =====================
# DASHBOARD
# =====================

st.subheader("📈 AI Trading Dashboard")

symbol = st.selectbox(
    "Select Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"
    ]
)


# =====================
# BITGET CANDLES
# =====================

def get_candles(symbol):

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity=1h&limit=100"
    )

    data = requests.get(url).json()

    df = pd.DataFrame(data["data"])

    df = df.iloc[:, :6]

    df.columns = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    df["close"] = df["close"].astype(float)

    return df


# =====================
# RSI
# =====================

def calculate_rsi(prices):

    delta = prices.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = (
        gain.rolling(14).mean()
        /
        loss.rolling(14).mean()
    )

    return 100 - (100/(1+rs))


# =====================
# RUN
# =====================

if st.button("🤖 Run AI Analysis"):

    df = get_candles(symbol)

    df["RSI"] = calculate_rsi(df["close"])

    price = df["close"].iloc[-1]

    current_rsi = df["RSI"].iloc[-1]


    if current_rsi < 30:
        signal = "BUY 🟢"
        risk = "Medium"

    elif current_rsi > 70:
        signal = "SELL 🔴"
        risk = "High"

    else:
        signal = "HOLD 🟡"
        risk = "Low"


    st.metric("Price", price)

    st.metric(
        "RSI",
        round(current_rsi,2)
    )

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


    try:

        response = client.chat.completions.create(

            model="qwen-plus",

            messages=[

                {
                    "role":"system",
                    "content":
                    "You are a crypto trading assistant."
                },

                {
                    "role":"user",
                    "content":
                    f"""
Analyze crypto:

Pair: {symbol}

Price: {price}

RSI: {round(current_rsi,2)}

Signal: {signal}

Risk: {risk}
"""
                }
            ]
        )


        st.subheader(
            "🧠 Qwen AI Analysis"
        )

        st.write(
            response.choices[0].message.content
        )


    except Exception as e:

        st.error(
            f"Qwen AI Error: {e}"
        )
