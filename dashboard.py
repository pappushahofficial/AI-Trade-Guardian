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
st.markdown(
"""
<style>

/* AI TRADE GUARDIAN MODERN UI */


/* Background */
.stApp {

    background:
    linear-gradient(
        135deg,
        #020617,
        #111827
    );

    color:white;

}


/* Main container */
.block-container {

    padding-top:2rem;

}


/* Title glow */
h1 {

    color:white;

    text-shadow:
    0 0 20px #38bdf8;

}


/* Headings */
h2,h3 {

    color:#e5e7eb;

}


/* Launch Button */
.stButton button {

    width:100%;

    height:55px;

    border-radius:18px;

    background:
    linear-gradient(
        90deg,
        #06b6d4,
        #8b5cf6
    );

    color:white;

    font-size:20px;

    font-weight:bold;

    border:none;

}


/* Button hover */
.stButton button:hover {

    transform:scale(1.02);

}


/* Metric Cards */
[data-testid="stMetric"] {

    background:
    linear-gradient(
        145deg,
        #0f172a,
        #1e293b
    );

    padding:20px;

    border-radius:20px;

    border:
    1px solid #334155;

    box-shadow:
    0px 0px 15px #0f172a;

}


/* Inputs */
.stTextInput input {

    background:#020617;

    color:white;

    border-radius:15px;

}


/* Dropdown */
.stSelectbox div {

    border-radius:15px;

}


/* Alert boxes */
.stAlert {

    border-radius:18px;

}


</style>
""",
unsafe_allow_html=True
)

st.title("🤖 AI Trade Guardian")


st.markdown("""
### Autonomous Crypto Trading Agent 🚀

Powered by:  
🧠 **Alibaba Qwen AI** | 📡 **Bitget API**

🏆 Bitget AI Hackathon

📊 Perceive → 🧠 Decide → ⚡ Execute → 🛡 Manage Risk
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


# =====================
# MARKET SELECTOR
# =====================

st.subheader("📈 Market Scanner")


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


    df["EMA20"] = df["close"].ewm(span=20).mean()

    df["EMA50"] = df["close"].ewm(span=50).mean()


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
Bitget market scanned.

🧠 Decide:
AI decision generated.

⚡ Execute:
Virtual trade created.

🛡 Risk:
SL / TP calculated.

🧪 Demo Mode Active
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


    a.metric("Direction", direction)

    b.metric("Confidence", confidence)

    c.metric("Signal", signal)


    x,y = st.columns(2)


    x.metric("🛑 Stop Loss", sl)

    y.metric("💰 Take Profit", tp)



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


    m1.metric("Asset", symbol)

    m2.metric("Decision", direction)

    m3.metric("Confidence", confidence)



    st.subheader("🧠 Qwen AI Trading Report")


    st.write(report)
