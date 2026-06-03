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


QWEN_API_KEY = os.getenv("BITGET_QWEN_API_KEY")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)


st.subheader("🔗 Connection Status")


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


st.subheader("📈 Trading Dashboard")


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



if st.button("🤖 Run AI Analysis"):


    with st.spinner("🧠 Qwen AI analysing market..."):


        df = get_candles(symbol)


        df["RSI"] = calculate_rsi(
            df["close"]
        )


        price = df["close"].iloc[-1]

        current_rsi = df["RSI"].iloc[-1]



        if current_rsi < 30:

            signal = "BUY 🟢"
            direction = "LONG 📈"
            risk = "Medium"

            stop_loss = price * 0.98
            take_profit = price * 1.04



        elif current_rsi > 70:

            signal = "SELL 🔴"
            direction = "SHORT 📉"
            risk = "High"

            stop_loss = price * 1.02
            take_profit = price * 0.96



        else:

            signal = "HOLD 🟡"
            direction = "WAIT ⏳"
            risk = "Low"

            stop_loss = price * 0.98
            take_profit = price * 1.02




        response = client.chat.completions.create(

            model="qwen3.6-flash",

            messages=[

                {
                    "role":"system",
                    "content":
                    "You are an expert crypto trading AI agent."
                },


                {
                    "role":"user",

                    "content":

                    f"""
Create professional trading analysis.

Pair:
{symbol}

Price:
{price}

RSI:
{round(current_rsi,2)}

Signal:
{signal}

Trade Direction:
{direction}

Risk:
{risk}

Stop Loss:
{round(stop_loss,2)}

Take Profit:
{round(take_profit,2)}


Give:

📊 Technical Analysis

📈 Long/Short Reason

🎯 Entry Plan

🛑 Risk Management

📋 Final Trading Decision
"""
                }

            ]

        )



    col1,col2,col3 = st.columns(3)


    col1.metric(
        "💰 Price",
        round(price,2)
    )


    col2.metric(
        "📊 RSI",
        round(current_rsi,2)
    )


    col3.metric(
        "⚠️ Risk",
        risk
    )



    col4,col5 = st.columns(2)


    col4.metric(
        "🤖 Signal",
        signal
    )


    col5.metric(
        "📍 Direction",
        direction
    )



    col6,col7 = st.columns(2)


    col6.metric(
        "🛑 Stop Loss",
        round(stop_loss,2)
    )


    col7.metric(
        "🎯 Take Profit",
        round(take_profit,2)
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
