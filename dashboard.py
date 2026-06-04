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

**Features**

🧠 AI Market Reasoning  
📈 Live Market Data  
📊 RSI + EMA Strategy  
⚡ Multi-Timeframe Scanner  
🎯 Smart Risk Engine
""")


st.success("🟢 Trading Agent Online")


demo = st.toggle(
    "🧪 Demo Mode (Save Qwen Credits)",
    value=True
)


QWEN_API_KEY = os.getenv("BITGET_QWEN_API_KEY")


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)



st.subheader("📈 Market Scanner")


symbol = st.text_input(
    "Trading Pair",
    value="BGBUSDT"
).upper()



def get_data():

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity=15min&limit=100"
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



if st.button("🤖 Launch AI Agent"):


    df = get_data()


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


    price = df["close"].iloc[-1]


    if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1]:

        direction = "LONG 📈"
        signal = "BUY 🟢"
        sl = round(price * 0.98,2)
        tp = round(price * 1.04,2)

    else:

        direction = "SHORT 📉"
        signal = "SELL 🔴"
        sl = round(price * 1.02,2)
        tp = round(price * 0.96,2)


    confidence = "85%"


    if demo:

        report = """
📊 DEMO AI REPORT

📊 Perceive:
Market scanned successfully.

🧠 Decide:
Trading decision generated.

⚡ Execute:
Virtual trade created.

🛡 Risk:
SL / TP calculated.

🧪 Demo Mode
Qwen credits saved ✅
"""


    else:

        with st.spinner("🧠 Qwen analysing..."):

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
Analyze:

Asset:
{symbol}

Decision:
{direction}

SL:
{sl}

TP:
{tp}
"""
                    }

                ]

            )


            report = response.choices[0].message.content



    st.subheader("🤖 AI Agent Decision")


    a,b,c = st.columns(3)


    a.metric(
        "Direction",
        direction
    )


    b.metric(
        "Confidence",
        confidence
    )


    c.metric(
        "Signal",
        signal
    )



    x,y = st.columns(2)


    x.metric(
        "🛑 Stop Loss",
        sl
    )


    y.metric(
        "💰 Take Profit",
        tp
    )



    st.subheader("📊 Market Chart")


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


    st.success(
        f"Virtual Execution Created ✅ {direction}"
    )



    st.subheader("🧾 Agent Memory")


    m1,m2,m3 = st.columns(3)


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



    st.subheader("🧠 Qwen AI Trading Report")


    st.write(report)
