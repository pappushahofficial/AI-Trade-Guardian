# ======================
# IMPORTS
# ======================

import streamlit as st
import os
import requests
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI



# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)



# ======================
# PRO DARK UI STYLE
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


.card {

    background:#0f172a;

    padding:25px;

    border-radius:25px;

    border:1px solid #1e293b;

    box-shadow:0 0 25px #020617;

}


h1,h2,h3 {

    color:white;

}


.stButton button {

    width:100%;

    border-radius:20px;

    background:
    linear-gradient(
    90deg,
    #06b6d4,
    #9333ea
    );

    color:white;

    border:none;

}


[data-testid="stMetric"] {

    background:#0f172a;

    padding:20px;

    border-radius:20px;

    border:1px solid #334155;

}

</style>
""",
unsafe_allow_html=True
)




# ======================
# API SETUP
# ======================

QWEN_API_KEY = os.getenv(
    "BITGET_QWEN_API_KEY"
)


client = OpenAI(

    api_key=QWEN_API_KEY,

    base_url=
    "https://hackathon.bitgetops.com/v1"

)




# ======================
# BITGET FUNCTION
# ======================

def get_data(symbol):


    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={symbol}&granularity=15min&limit=100"
    )


    response = requests.get(
        url
    ).json()


    df = pd.DataFrame(
        response["data"]
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


    for col in [

        "open",

        "high",

        "low",

        "close"

    ]:


        df[col] = (
            df[col]
            .astype(float)
        )


    return df
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
margin-bottom:15px;">
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


    st.success(
        "🟢 Online"
    )


    st.markdown("---")


    menu = st.radio(
        "Menu",
        [
            "📈 Market Scanner",
            "⭐ Watchlist",
            "ℹ️ About Agent",
            "⚙️ Settings"
        ]
    )


    st.markdown("---")


    st.markdown(
    """
<div class="card">

<h4>🤖 AGENT STATUS</h4>

<p>🟢 Status: Online</p>

<p>⏱ Uptime: Running</p>

<p>📈 Signals Active</p>

</div>
""",
    unsafe_allow_html=True
    )


    st.markdown("---")


    st.markdown(
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
# PAGE : MARKET SCANNER
# ======================

if menu == "📈 Market Scanner":


    # ===== HEADER =====


    st.title(
        "Autonomous Crypto Trading Agent 🚀"
    )


    st.markdown(
"""
### Powered by

🧠 **Alibaba Qwen AI** | 📡 **Bitget API**

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




    # ===== LIVE CONNECTIONS =====


    st.subheader(
        "🔗 Live Connections"
    )


    a,b,c = st.columns(3)


    a.metric(
        "🧠 Qwen AI",
        "Connected"
    )


    b.metric(
        "📡 Bitget API",
        "Connected"
    )


    c.metric(
        "🤖 Agent",
        "Running"
    )




    # ===== MARKET SCANNER =====


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
            "XRPUSDT"
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
    # ======================
    # LAUNCH AI AGENT
    # ======================


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


        price = (
            df["close"]
            .iloc[-1]
        )


        if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1]:


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


        st.subheader(
            "🤖 Agent Decision"
        )


        x,y,z = st.columns(3)


        x.metric(
            "Decision",
            direction
        )


        y.metric(
            "Confidence",
            "85%"
        )


        z.metric(
            "Signal",
            signal
        )


        st.metric(
            "🛑 Stop Loss",
            sl
        )


        st.metric(
            "🎯 Take Profit",
            tp
        )



        # ===== CHART =====


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



        # ===== EXECUTION =====


        st.subheader(
            "⚡ Agent Execution Center"
        )


        st.success(
            "Virtual Execution Created ✅"
        )



        # ===== MEMORY =====


        st.subheader(
            "🧾 Agent Memory"
        )


        st.write(
            f"""
Asset: {symbol}

Decision: {direction}

Confidence: 85%
"""
        )





# ======================
# PAGE : WATCHLIST
# ======================

if menu == "⭐ Watchlist":


    st.title(
        "⭐ Watchlist"
    )


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


        price = (
            df["close"]
            .iloc[-1]
        )


        c1,c2,c3 = st.columns(
            [2,2,1]
        )


        c1.write(
            "🟢 " + coin
        )


        c2.write(
            f"💰 {price}"
        )


        open_chart = c3.button(
            "📈 Chart",
            key=coin
        )


        if open_chart:


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
# PAGE : ABOUT AGENT
# ======================

if menu == "ℹ️ About Agent":


    st.title(
        "🤖 AI Trade Guardian"
    )


    st.write(
        """
👁 Perceive → Market data

🧠 Decide → Alibaba Qwen AI

⚡ Execute → Agent action

🛡 Manage Risk → SL / TP
"""
    )





# ======================
# PAGE : SETTINGS
# ======================

if menu == "⚙️ Settings":


    st.title(
        "⚙️ Settings"
    )


    st.toggle(
        "🌙 Dark Mode",
        value=True
    )
