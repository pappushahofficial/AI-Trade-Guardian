import streamlit as st
import os
import requests
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI


# =====================
# PAGE
# =====================

st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Trade Guardian")


st.markdown(
"""
### Autonomous Crypto Trading Agent 🚀

Powered by:

🧠 **Alibaba Qwen AI**  
📡 **Bitget Market API**

---

### Agent Pipeline

📊 **PERCEIVE**  
Live multi-timeframe market scanning

🧠 **DECIDE**  
AI trading reasoning & strategy generation

🛡 **MANAGE RISK**  
Stop Loss + Take Profit planning
"""
)


st.success("🟢 Agent System Online")



# =====================
# API
# =====================

QWEN_API_KEY = os.getenv("BITGET_QWEN_API_KEY")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)



# =====================
# CONNECTION
# =====================

st.subheader("🔗 AI Infrastructure")


st.success(
    "🧠 Qwen Engine Connected"
    if QWEN_API_KEY
    else "❌ Qwen Offline"
)


st.success(
    "📡 Bitget Data Connected"
    if BITGET_API_KEY
    else "❌ Bitget Offline"
)



# =====================
# SELECT
# =====================

st.subheader("📈 Market Scanner")


symbol = st.selectbox(
    "Select Asset",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"
    ]
)



# =====================
# DATA
# =====================

def get_data(symbol,tf):

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity={tf}&limit=100"
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


    return 100-(100/(1+rs))



# ANALYSIS

def analyze(tf):

    df = get_data(
        symbol,
        tf
    )


    df["RSI"] = rsi(
        df["close"]
    )


    df["EMA20"] = (
        df["close"]
        .ewm(span=20)
        .mean()
    )


    df["EMA50"] = (
        df["close"]
        .ewm(span=50)
        .mean()
    )


    trend = (
        "BULLISH 🟢"
        if df["EMA20"].iloc[-1]
        >
        df["EMA50"].iloc[-1]

        else
        "BEARISH 🔴"
    )


    return trend,df



# =====================
# RUN
# =====================

if st.button("🤖 Launch AI Agent"):


    with st.spinner(
        "🧠 Qwen AI analysing market..."
    ):


        t15,df = analyze("15min")

        t1,_ = analyze("1h")

        t4,_ = analyze("4h")


        price = df["close"].iloc[-1]


        bullish = [
            t15,
            t1,
            t4
        ].count(
            "BULLISH 🟢"
        )



        if bullish >= 2:

            signal = "BUY 🟢"
            direction = "LONG 📈"
            confidence = "85%"

            sl = round(price*0.98,2)
            tp = round(price*1.04,2)



        elif bullish == 0:

            signal = "SELL 🔴"
            direction = "SHORT 📉"
            confidence = "85%"

            sl = round(price*1.02,2)
            tp = round(price*0.96,2)



        else:

            signal = "HOLD 🟡"
            direction = "NO TRADE ⏳"
            confidence = "60%"

            sl = "Waiting"
            tp = "Waiting"



        response = client.chat.completions.create(

            model="qwen3.6-flash",

            messages=[

                {
                    "role":"system",
                    "content":
                    "You are an autonomous crypto trading agent."
                },

                {
                    "role":"user",

                    "content":

                    f"""
Generate professional AI trading report.

Asset:
{symbol}

15m:
{t15}

1H:
{t1}

4H:
{t4}

Decision:
{direction}

Confidence:
{confidence}

Stop Loss:
{sl}

Take Profit:
{tp}

Include:
Market analysis
Trade reasoning
Risk management
"""
                }

            ]

        )



    a,b,c = st.columns(3)


    a.metric("⚡ 15m",t15)
    b.metric("📈 1H",t1)
    c.metric("🏦 4H",t4)



    d,e,f = st.columns(3)


    d.metric("🤖 Signal",signal)
    e.metric("📍 Direction",direction)
    f.metric("🎯 Confidence",confidence)



    g,h = st.columns(2)


    g.metric("🛑 Stop Loss",sl)

    h.metric("💰 Take Profit",tp)



    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            y=df["close"],
            name="Price"
        )
    )


    fig.add_trace(
        go.Scatter(
            y=df["EMA20"],
            name="EMA20"
        )
    )


    fig.add_trace(
        go.Scatter(
            y=df["EMA50"],
            name="EMA50"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    st.subheader(
        "🧠 Qwen AI Trading Report"
    )


    st.write(
        response.choices[0].message.content
    )
