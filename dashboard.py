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


st.markdown(
"""
### Autonomous Crypto Trading Agent 🚀

Powered by:  
🧠 **Alibaba Qwen AI** | 📡 **Bitget API**

🏆 **Bitget AI Hackathon**

📊 Perceive → 🧠 Decide → ⚡ Execute → 🛡 Manage Risk

**Features**

🧠 AI Market Reasoning  
📈 Live Market Data  
📊 RSI + EMA Strategy  
⚡ Multi-Timeframe Scanner  
🎯 Smart Risk Engine
"""
)


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



st.subheader("🔗 Live Connections")


st.success(
    "🧠 Qwen AI Connected"
    if QWEN_API_KEY
    else "❌ Qwen Offline"
)



st.subheader("📈 Market Scanner")


default_pair = st.selectbox(
    "Popular Assets",
    [
        "BTCUSDT",
        "ETHUSDT",
        "BGBUSDT",
        "SOLUSDT",
        "BNBUSDT",
        "XRPUSDT",
        "DOGEUSDT",
        "ADAUSDT"
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



def get_data(symbol,tf):

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



def rsi(price):

    delta = price.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    rs = (
        gain.rolling(14).mean()
        /
        loss.rolling(14).mean()
    )

    return 100-(100/(1+rs))



def scan(tf):

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



if st.button("🤖 Launch AI Agent"):


    t15,df = scan("15min")

    t1,_ = scan("1h")

    t4,_ = scan("4h")


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
        sl = round(price*0.98,2)
        tp = round(price*1.04,2)


    elif score == 0:

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
        if demo_mode:

        response = type(
            "DemoResponse",
            (),
            {
                "choices": [
                    type(
                        "Choice",
                        (),
                        {
                            "message": type(
                                "Message",
                                (),
                                {
                                    "content": """
📊 DEMO AI TRADING REPORT

🤖 AI Trade Guardian Simulation

📊 PERCEIVE:
Market data analysed.

🧠 DECIDE:
AI generated trading decision.

⚡ EXECUTE:
Virtual trade action created.

🛡 RISK:
Stop Loss and Take Profit prepared.

🧪 Demo Mode Active
Qwen credits saved ✅
"""
                                }
                            )()
                        }
                    )()
                ]
            }
        )()
