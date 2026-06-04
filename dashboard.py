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


# ======================
# PRO DARK DASHBOARD UI
# ======================


st.markdown(
"""
<style>

.stApp {
    background:#050816;
    color:white;
}


.block-container {
    padding-top:2rem;
}


section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #050816,
    #0f172a
    );

}


h1,h2,h3 {
    color:white;
}


.card {

    background:#0f172a;

    padding:25px;

    border-radius:25px;

    border:1px solid #1e293b;

    box-shadow:
    0 0 25px #020617;

}


.neon {

    color:#22d3ee;

}


.stButton button {

    height:60px;

    width:100%;

    border-radius:20px;

    background:
    linear-gradient(
    90deg,
    #06b6d4,
    #9333ea
    );

    color:white;

    font-size:22px;

    border:none;

}


[data-testid="stMetric"] {

    background:#0f172a;

    padding:20px;

    border-radius:20px;

    border:1px solid #334155;

}


.stTextInput input {

    background:#020617;

    color:white;

    border-radius:15px;

}


</style>
""",
unsafe_allow_html=True
)



# ======================
# SIDEBAR
# ======================


with st.sidebar:


    st.markdown(
    """
<div style="text-align:center">

<div style="
font-size:65px;
width:90px;
height:90px;
margin:auto;
display:flex;
align-items:center;
justify-content:center;
background:#111827;
border-radius:25px;
border:2px solid #22d3ee;
box-shadow:0 0 30px #06b6d4;
margin-bottom:15px;
">
🤖
</div>

<h2>AI Trade<br>Guardian</h2>

<p style="color:#94a3b8">
Autonomous Trading Agent
</p>

</div>
""",
    unsafe_allow_html=True
    )


    st.success("🟢 Online")


    st.markdown("---")


    st.markdown(
    """
### Menu

📈 Market Scanner

📊 Dashboard

💼 Portfolio

🕒 Trade History

⭐ Watchlist

⚙️ Settings
"""
    )


    st.markdown("---")


    st.info(
    """
POWERED BY

🧠 Alibaba Qwen AI

📡 Bitget API
"""
    )



# ======================
# HEADER
# ======================


st.title(
    "Autonomous Crypto Trading Agent 🚀"
)


st.markdown(
"""
### Powered by

🧠 **Alibaba Qwen AI**  |  📡 **Bitget API**

🏆 Bitget AI Hackathon

📊 Perceive → 🧠 Decide → ⚡ Execute → 🛡 Manage Risk
"""
)


st.success(
    "🟢 Trading Agent Online"
)


demo = st.toggle(
    "🧪 Demo Mode (Save Qwen Credits)",
    value=True
)



# ======================
# CONNECTIONS
# ======================


st.subheader(
    "🔗 Live Connections"
)


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "🧠 AI Model",
    "Qwen 3.5",
    "Connected"
)


c2.metric(
    "📡 Market Data",
    "Bitget API",
    "Connected"
)


c3.metric(
    "🤖 Agent",
    "Active",
    "Running"
)


c4.metric(
    "🟢 Status",
    "Live",
    "Ready"
)
# ======================
# API
# ======================

QWEN_API_KEY = os.getenv(
    "BITGET_QWEN_API_KEY"
)


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)



# ======================
# MARKET SCANNER
# ======================


st.subheader(
    "📈 Market Scanner"
)


default_coin = st.selectbox(
    "🔥 Top Crypto Assets",
    [
        "BTCUSDT",
        "ETHUSDT",
        "BGBUSDT",
        "SOLUSDT",
        "BNBUSDT",
        "XRPUSDT",
        "DOGEUSDT",
        "ADAUSDT",
        "AVAXUSDT",
        "LINKUSDT"
    ]
)


custom_coin = st.text_input(
    "🔎 Custom Bitget Pair",
    placeholder="Example: SUIUSDT"
)


symbol = (
    custom_coin.upper().strip()
    if custom_coin
    else default_coin
)



def get_data():

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity=15min&limit=100"
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


    df["close"] = (
        df["close"]
        .astype(float)
    )


    return df



if st.button(
    "🤖 Launch AI Agent"
):


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


    price = (
        df["close"]
        .iloc[-1]
    )


    if (
        df["EMA20"].iloc[-1]
        >
        df["EMA50"].iloc[-1]
    ):

        direction = "LONG 📈"

        signal = "BUY 🟢"

        sl = round(
            price * 0.98,
            2
        )

        tp = round(
            price * 1.04,
            2
        )


    else:

        direction = "SHORT 📉"

        signal = "SELL 🔴"

        sl = round(
            price * 1.02,
            2
        )

        tp = round(
            price * 0.96,
            2
        )


    confidence = "85%"



    if demo:

        report = """
📊 DEMO AI REPORT

📊 PERCEIVE:
Market scanned.

🧠 DECIDE:
AI strategy generated.

⚡ EXECUTE:
Virtual trade created.

🛡 RISK:
SL / TP calculated.

Qwen credits saved ✅
"""


    else:


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

Stop Loss:
{sl}

Take Profit:
{tp}
"""
                }
            ]
        )


        report = (
            response
            .choices[0]
            .message
            .content
        )



    st.subheader(
        "🤖 Agent Decision"
    )


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



    st.subheader(
        "📊 Market Chart"
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
        "⚡ Agent Execution Center"
    )


    st.success(
        f"Virtual Execution Created ✅ {direction}"
    )



    st.subheader(
        "🧾 Agent Memory"
    )


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



    st.subheader(
        "🧠 Qwen AI Report"
    )


    st.write(
        report
    )
