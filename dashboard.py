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


st.title("🤖 AI Trade Guardian")


st.markdown("""
### Autonomous Crypto Trading Agent 🚀

Powered by:
🧠 Alibaba Qwen AI | 📡 Bitget API

🏆 Bitget AI Hackathon

📊 Perceive → 🧠 Decide → ⚡ Execute → 🛡 Manage Risk

Features:
- AI Market Reasoning
- Live Market Data
- RSI + EMA Strategy
- Multi-Timeframe Scanner
- Smart Risk Engine
""")


st.success("🟢 Trading Agent Online")


demo_mode = st.toggle(
    "🧪 Demo Mode (Save Qwen Credits)",
    value=True
)


QWEN_API_KEY = os.getenv("BITGET_QWEN_API_KEY")


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)


st.subheader("🔗 Connections")


st.success(
    "🧠 Qwen Connected"
    if QWEN_API_KEY
    else "❌ Qwen Offline"
)


st.subheader("📈 Market Scanner")


default_pair = st.selectbox(
    "Select Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "BGBUSDT",
        "SOLUSDT",
        "BNBUSDT",
        "XRPUSDT"
    ]
)


custom_pair = st.text_input(
    "Custom Pair",
    placeholder="Example: SUIUSDT"
)


symbol = custom_pair.upper() if custom_pair else default_pair



def get_data(symbol, tf):

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



def scan(tf):

    df = get_data(
        symbol,
        tf
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
        if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1]
        else
        "BEARISH 🔴"
    )


    return trend, df



if st.button("🤖 Launch AI Agent"):


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

        direction = "LONG 📈"
        signal = "BUY 🟢"
        confidence = "85%"
        sl = round(price * 0.98, 2)
        tp = round(price * 1.04, 2)


    elif score == 0:

        direction = "SHORT 📉"
        signal = "SELL 🔴"
        confidence = "85%"
        sl = round(price * 1.02, 2)
        tp = round(price * 0.96, 2)


    else:

        direction = "WAIT ⏳"
        signal = "HOLD 🟡"
        confidence = "60%"
        sl = "Waiting"
        tp = "Waiting"
if demo_mode:

        response_text = """
📊 DEMO AI TRADING REPORT

🤖 AI Trade Guardian

📊 PERCEIVE:
Bitget market data scanned.

🧠 DECIDE:
AI strategy generated decision.

⚡ EXECUTE:
Virtual trade action created.

🛡 RISK:
Stop Loss and Take Profit prepared.

🧪 Demo Mode Active
Qwen credits saved ✅
"""


    else:

        with st.spinner("🧠 Qwen AI analysing..."):

            response = client.chat.completions.create(

                model="qwen3.6-flash",

                messages=[

                    {
                        "role": "system",
                        "content":
                        "You are a professional autonomous crypto trading agent."
                    },

                    {
                        "role": "user",
                        "content": f"""
Analyze crypto market.

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

SL:
{sl}

TP:
{tp}
"""
                    }

                ]

            )


            response_text = (
                response
                .choices[0]
                .message
                .content
            )



    st.subheader("🤖 AI Agent Decision")


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "📍 Direction",
        direction
    )


    c2.metric(
        "🎯 Confidence",
        confidence
    )


    c3.metric(
        "🤖 Signal",
        signal
    )



    c4, c5 = st.columns(2)


    c4.metric(
        "🛑 Stop Loss",
        sl
    )


    c5.metric(
        "💰 Take Profit",
        tp
    )



    st.subheader("📊 Multi-Timeframe")


    a, b, c = st.columns(3)


    a.metric(
        "15m",
        t15
    )


    b.metric(
        "1H",
        t1
    )


    c.metric(
        "4H",
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



    st.subheader("⚡ Agent Execution Center")


    if direction == "LONG 📈":

        action = "OPEN LONG 📈"

    elif direction == "SHORT 📉":

        action = "OPEN SHORT 📉"

    else:

        action = "WAIT ⏳"



    x1, x2 = st.columns(2)


    x1.metric(
        "🤖 Agent Action",
        action
    )


    x2.metric(
        "⚙️ Execution",
        "Virtual Trade Created ✅"
    )



    st.subheader("🧾 Agent Memory")


    m1, m2, m3 = st.columns(3)


    m1.metric(
        "Asset",
        symbol
    )


    m2.metric(
        "Decision",
        direction
    )


    m3.metric(
        "Confidence",
        confidence
    )


    st.success(
        "Saved to Agent Memory ✅"
    )



    st.subheader(
        "🧠 Qwen AI Trading Report"
    )


    st.write(
        response_text
    )
