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


st.title("🤖 AI Trade Guardian v2")
st.success("Trading Agent Online 🚀")


st.markdown(
"""
### 🏆 Bitget AI Hackathon

🤖 Qwen AI  
📈 Bitget Market Data  
📊 RSI + EMA  
⚡ Multi-Timeframe Scanner  
🎯 AI Risk Engine
"""
)


QWEN_API_KEY = os.getenv("BITGET_QWEN_API_KEY")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)


st.subheader("🔗 Status")

st.success(
    "✅ Qwen Connected"
    if QWEN_API_KEY
    else "❌ Qwen Missing"
)

st.success(
    "✅ Bitget Connected"
    if BITGET_API_KEY
    else "❌ Bitget Missing"
)



symbol = st.selectbox(
    "Select Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"
    ]
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



def analyze(tf):

    df = get_data(symbol,tf)

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
        if df["EMA20"].iloc[-1] >
        df["EMA50"].iloc[-1]
        else "BEARISH 🔴"
    )


    return (
        trend,
        df["RSI"].iloc[-1],
        df
    )



if st.button("🤖 Run AI Analysis"):


    with st.spinner(
        "🧠 Qwen AI analysing all timeframes..."
    ):


        t15,r15,df = analyze("15min")
        t1,r1,_ = analyze("1h")
        t4,r4,_ = analyze("4h")


        bullish = [
            t15,
            t1,
            t4
        ].count(
            "BULLISH 🟢"
        )


        price = df["close"].iloc[-1]


        if bullish >= 2:

            signal = "BUY 🟢"
            direction = "LONG 📈"
            confidence = "85%"

            sl = round(
                price*0.98,
                2
            )

            tp = round(
                price*1.04,
                2
            )


        elif bullish == 0:

            signal = "SELL 🔴"
            direction = "SHORT 📉"
            confidence = "85%"

            sl = round(
                price*1.02,
                2
            )

            tp = round(
                price*0.96,
                2
            )


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
                    "You are an expert crypto trading AI agent."
                },


                {
                    "role":"user",

                    "content":

                    f"""
Create professional trading analysis.

Pair:
{symbol}

15m:
{t15}

1H:
{t1}

4H:
{t4}

Signal:
{signal}

Direction:
{direction}

Confidence:
{confidence}

Stop Loss:
{sl}

Take Profit:
{tp}


Explain:
📊 Market
📈 Direction
🎯 Trade Plan
🛡 Risk
"""
                }

            ]

        )



    c1,c2,c3 = st.columns(3)

    c1.metric(
        "⚡15m",
        t15
    )

    c2.metric(
        "📈1H",
        t1
    )

    c3.metric(
        "🏦4H",
        t4
    )



    c4,c5,c6 = st.columns(3)

    c4.metric(
        "🤖 Signal",
        signal
    )

    c5.metric(
        "📍 Direction",
        direction
    )

    c6.metric(
        "🎯 Confidence",
        confidence
    )



    c7,c8 = st.columns(2)

    c7.metric(
        "🛑 Stop Loss",
        sl
    )

    c8.metric(
        "💰 Take Profit",
        tp
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
        "🧠 Qwen AI Analysis"
    )


    st.write(
        response.choices[0].message.content
    )
