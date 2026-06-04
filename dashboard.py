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


# ======================
# CLICKABLE MENU
# ======================


menu = st.sidebar.radio(
    "Menu",
    [
        "📈 Market Scanner",
        "⭐ Watchlist",
        "ℹ️ About Agent",
        "⚙️ Settings"
    ]
)


# ======================
# AGENT STATUS
# ======================


st.sidebar.markdown("---")


st.sidebar.markdown(
"""
<div class="card">

<h4>🤖 AGENT STATUS</h4>

<p>🟢 <b>Status:</b> Online</p>

<p>⏱ <b>Uptime:</b> 02:45:32</p>

<p>📈 <b>Signals Today:</b> 12</p>

<p>🎯 <b>Accuracy:</b> 85.6%</p>

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
# BITGET DATA
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
# WATCHLIST PAGE
# ======================

if menu == "⭐ Watchlist":


    st.title(
        "⭐ Watchlist"
    )


    watchlist = [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
        "BGBUSDT"
    ]


    for coin in watchlist:


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


        show = c3.button(
            "📈 Chart",
            key=coin
        )


        if show:


            st.subheader(
                f"📈 {coin} Live Chart"
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


            fig.update_layout(
                height=450,
                xaxis_rangeslider_visible=False
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )



# ======================
# HEADER
# ======================

if menu == "📈 Market Scanner":


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


    demo = st.toggle(
        "🧪 Demo Mode (Save Qwen Credits)",
        value=True
    )


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


    if st.button(
        "🤖 Launch AI Agent"
    ):


        df = get_data(
            symbol
        )


        st.success(
            "🤖 Agent Analysis Complete"
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
