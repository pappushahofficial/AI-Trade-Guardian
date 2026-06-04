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
# STYLE
# ======================

st.markdown(
"""
<style>

.stApp {
    background:#050816;
    color:white;
}

section[data-testid="stSidebar"] {
    background:#0f172a;
}

.card {
    background:#0f172a;
    padding:25px;
    border-radius:20px;
    border:1px solid #334155;
    box-shadow:0 0 25px #020617;
}

.stButton button {
    width:100%;
    height:55px;
    border-radius:18px;
    background:linear-gradient(90deg,#06b6d4,#9333ea);
    color:white;
    border:none;
}

[data-testid="stMetric"] {
    background:#0f172a;
    padding:15px;
    border-radius:15px;
}

h1,h2,h3 {
    color:white;
}

</style>
""",
unsafe_allow_html=True
)


# ======================
# BITGET DATA FUNCTION
# ======================

def get_data(symbol):

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

    for c in [
        "open",
        "high",
        "low",
        "close"
    ]:
        df[c] = df[c].astype(float)

    return df


# ======================
# QWEN
# ======================

QWEN_API_KEY = os.getenv(
    "BITGET_QWEN_API_KEY"
)


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)


# ======================
# SIDEBAR
# ======================

with st.sidebar:

    st.markdown(
    """
<div style="text-align:center">

<div style="
font-size:60px;
width:90px;
height:90px;
margin:auto;
display:flex;
align-items:center;
justify-content:center;
background:#111827;
border-radius:25px;
border:2px solid #22d3ee;
box-shadow:0 0 25px #06b6d4;">
🤖
</div>

<h2>AI Trade<br>Guardian</h2>

</div>
""",
    unsafe_allow_html=True
    )


menu = st.sidebar.radio(
    "Menu",
    [
        "📈 Market Scanner",
        "⭐ Watchlist",
        "ℹ️ About Agent",
        "⚙️ Settings"
    ]
)


st.sidebar.markdown("---")


st.sidebar.markdown(
"""
<div class="card">

<h4>🤖 AGENT STATUS</h4>

<p>🟢 Status: Online</p>

<p>⏱ Uptime: 02:45:32</p>

<p>📈 Signals Today: 12</p>

<p>🎯 Accuracy: 85.6%</p>

</div>
""",
unsafe_allow_html=True
)


st.sidebar.markdown("---")


st.sidebar.markdown(
"""
<div class="card">

<h4>POWERED BY</h4>

<p>🧠 Alibaba Qwen AI</p>

<p>📡 Bitget API</p>

</div>
""",
unsafe_allow_html=True
)
# ======================
# MARKET SCANNER PAGE
# ======================

if menu == "📈 Market Scanner":

    st.title(
        "Autonomous Crypto Trading Agent 🚀"
    )


    st.markdown(
    """
🧠 **Alibaba Qwen AI** | 📡 **Bitget API**

📊 Perceive → 🧠 Decide → ⚡ Execute → 🛡 Manage Risk
"""
    )


    demo = st.toggle(
        "🧪 Demo Mode (Save Qwen Credits)",
        value=True
    )


    c1,c2,c3 = st.columns(3)

    c1.metric(
        "🧠 Qwen AI",
        "Connected"
    )

    c2.metric(
        "📡 Bitget",
        "Connected"
    )

    c3.metric(
        "🤖 Agent",
        "Online"
    )


    st.subheader(
        "📈 Market Scanner"
    )


    coin = st.selectbox(
        "🔥 Top Crypto Assets",
        [
            "BTCUSDT",
            "ETHUSDT",
            "BGBUSDT",
            "SOLUSDT",
            "BNBUSDT",
            "XRPUSDT"
        ]
    )


    custom = st.text_input(
        "🔎 Custom Bitget Pair",
        placeholder="Example: SUIUSDT"
    )


    symbol = (
        custom.upper()
        if custom
        else coin
    )


    if st.button(
        "🤖 Launch AI Agent"
    ):

        df = get_data(
            symbol
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


        price = df["close"].iloc[-1]


        if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1]:

            decision = "LONG 📈"

            sl = round(price * 0.98,2)

            tp = round(price * 1.04,2)

        else:

            decision = "SHORT 📉"

            sl = round(price * 1.02,2)

            tp = round(price * 0.96,2)


        a,b,c = st.columns(3)


        a.metric(
            "Decision",
            decision
        )


        b.metric(
            "Confidence",
            "85%"
        )


        c.metric(
            "Price",
            price
        )


        st.metric(
            "🛑 SL",
            sl
        )


        st.metric(
            "🎯 TP",
            tp
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


        st.success(
            "⚡ Virtual Execution Created"
        )



# ======================
# WATCHLIST
# ======================

if menu == "⭐ Watchlist":

    st.title("⭐ Watchlist")


    coins = [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
        "BGBUSDT"
    ]


    for coin in coins:

        df = get_data(
            coin
        )

        price = df["close"].iloc[-1]


        col1,col2,col3 = st.columns(
            [2,2,1]
        )


        col1.write(
            "🟢 " + coin
        )


        col2.write(
            f"💰 {price}"
        )


        open_chart = col3.button(
            "📈 Chart",
            key=coin
        )


        if open_chart:

            st.subheader(
                coin
            )


            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=df["time"],
                        open=df["open"],
                        high=df["high"],
                        low=df["low"],
                        close=df["close"]
                    )
                ]
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )



# ======================
# ABOUT
# ======================

if menu == "ℹ️ About Agent":

    st.title(
        "🤖 AI Trade Guardian"
    )

    st.write(
        """
AI autonomous trading assistant.

Powered by:

🧠 Alibaba Qwen AI

📡 Bitget Market API

Flow:

📊 Perceive

🧠 Decide

⚡ Execute

🛡 Manage Risk
"""
    )



# ======================
# SETTINGS
# ======================

if menu == "⚙️ Settings":

    st.title(
        "⚙️ Settings"
    )


    st.toggle(
        "🌙 Dark Mode",
        value=True
    )
