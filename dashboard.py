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
st.success("System Online")


st.markdown(
"""
### 🚀 Bitget AI Hackathon Project

🤖 Qwen AI Intelligence  
📈 Bitget Live Market Data  
📊 RSI Technical Analysis  
⚠️ Risk Management System  

AI powered crypto market assistant.
"""
)


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

st.subheader("🔗 Connection Status")


st.success(
    "✅ Bitget Qwen Connected"
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
    "Select Trading Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"
    ]
)



def get_candles(symbol):

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity=1h&limit=100"
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


    gain = delta.clip(
        lower=0
    )


    loss = -delta.clip(
        upper=0
    )


    rs = (
        gain.rolling(14).mean()
        /
        loss.rolling(14).mean()
    )


    return 100 - (100/(1+rs))



if st.button("🤖 Run AI Analysis"):


    with st.spinner("🤖 Qwen AI is analysing market..."):


        df = get_candles(symbol)


        df["RSI"] = calculate_rsi(
            df["close"]
        )


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



        response = client.chat.completions.create(

            model="qwen3.6-flash",

            messages=[

                {
                    "role":"system",
                    "content":
                    "You are a crypto trading AI."
                },

                {
                    "role":"user",
                    "content":
                    f"""
Analyze shortly:

Pair: {symbol}
Price: {price}
RSI: {round(current_rsi,2)}
Signal: {signal}
Risk: {risk}

Reply under 5 lines.
"""
                }

            ]

        )



    col1,col2,col3 = st.columns(3)


    col1.metric(
        "💰 Price",
        price
    )


    col2.metric(
        "📊 RSI",
        round(current_rsi,2)
    )


    col3.metric(
        "⚠️ Risk",
        risk
    )


    st.metric(
        "🤖 Signal",
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


    st.subheader(
        "🧠 Qwen AI Analysis"
    )


    st.write(
        response.choices[0].message.content
    )
