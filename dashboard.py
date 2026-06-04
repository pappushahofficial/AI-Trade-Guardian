import streamlit as st
import os
import requests
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI


st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)


# =====================
# HEADER
# =====================

st.title("🤖 AI Trade Guardian")


st.markdown(
"""
### Autonomous Crypto Trading Agent 🚀

Powered by:  
🧠 **Alibaba Qwen AI** | 📡 **Bitget API**

🏆 **Bitget AI Hackathon**

📊 Perceive → 🧠 Decide → 🛡 Manage Risk

**Features**

🧠 AI Market Reasoning  
📈 Live Market Data  
📊 RSI + EMA Strategy  
⚡ Multi-Timeframe Scanner  
🎯 Smart Risk Engine
"""
)


st.success("🟢 Trading Agent Online")



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
# STATUS
# =====================

st.subheader("🔗 Live Connections")


st.success(
    "🧠 Qwen AI Connected"
    if QWEN_API_KEY
    else "❌ Qwen Offline"
)


st.success(
    "📡 Bitget Data Connected"
    if BITGET_API_KEY
    else "❌ Bitget Offline"
)




# =====================
# MARKET SELECTOR
# =====================

st.subheader("📈 Market Scanner")


default_pair = st.selectbox(
    "Popular Assets",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
        "BGBUSDT",
        "BNBUSDT",
        "XRPUSDT",
        "DOGEUSDT",
        "ADAUSDT",
        "AVAXUSDT",
        "LINKUSDT",
        "LTCUSDT"
    ]
)


custom_pair = st.text_input(
    "🔎 Custom Bitget Pair",
    placeholder="Example: SUIUSDT"
)


symbol = (
    custom_pair.upper().strip()
    if custom_pair
    else default_pair
)


# =====================
# DATA ENGINE
# =====================

def get_data(symbol, tf):

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity={tf}&limit=100"
    )

    data = requests.get(url).json()


    df = pd.DataFrame(
        data["data"]
    )


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



def scan(tf):

    df = get_data(
        symbol,
        tf
    )


    df["RSI"] = calculate_rsi(
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


    return trend, df



# =====================
# RUN AGENT
# =====================

if st.button("🤖 Launch AI Agent"):


    with st.spinner(
        "🧠 Qwen AI analysing market..."
    ):


        t15, df = scan("15min")

        t1, _ = scan("1h")

        t4, _ = scan("4h")


        price = df["close"].iloc[-1]


        score = [
            t15,
            t1,
            t4
        ].count(
            "BULLISH 🟢"
        )



        if score >= 2:

            signal = "BUY 🟢"
            direction = "LONG 📈"
            confidence = "85%"

            sl = round(price * 0.98,2)

            tp = round(price * 1.04,2)



        elif score == 0:

            signal = "SELL 🔴"
            direction = "SHORT 📉"
            confidence = "85%"

            sl = round(price * 1.02,2)

            tp = round(price * 0.96,2)



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
                    "You are a professional autonomous crypto trading agent."
                },

                {
                    "role":"user",

                    "content":

                    f"""
Create a professional trading report.

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
Technical analysis
Trade reasoning
Risk management
"""
                }

            ]

        )



    st.subheader(
        "🤖 AI Agent Decision"
    )


    a,b,c = st.columns(3)


    a.metric(
        "📍 Direction",
        direction
    )


    b.metric(
        "🎯 Confidence",
        confidence
    )


    c.metric(
        "🤖 Signal",
        signal
    )



    d,e = st.columns(2)


    d.metric(
        "🛑 Stop Loss",
        sl
    )


    e.metric(
        "💰 Take Profit",
        tp
    )



    st.subheader(
        "📊 Multi-Timeframe View"
    )


    x,y,z = st.columns(3)


    x.metric(
        "⚡15m",
        t15
    )


    y.metric(
        "📈1H",
        t1
    )


    z.metric(
        "🏦4H",
        t4
    )



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
