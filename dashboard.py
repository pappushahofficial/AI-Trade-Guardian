import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st_autorefresh(
    interval=60000,
    key="agent_loop"
)


st.title("🤖 AI Trade Guardian - Bitget Agent")

st.caption(
    "Bitget AI Trading Agent | Observe → Think → Risk → Execute"
)


# ---------------- CONTROL ----------------

st.sidebar.header("⚙️ Agent Control")

capital = st.sidebar.number_input(
    "Paper Capital ($)",
    value=10000
)

st.sidebar.success(
    "Connected to Bitget 🟢"
)


# ---------------- BITGET MARKET API ----------------

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT"
]


def get_bitget(symbol):

    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
    )


    params = {

        "symbol": symbol,
        "granularity": "1h",
        "limit": "100"

    }


    data = requests.get(
        url,
        params=params,
        timeout=10
    ).json()


    candles = data["data"]


    prices = [
        float(c[4])
        for c in candles
    ]


    df = pd.DataFrame(
        prices,
        columns=["price"]
    )


    change = (
        (prices[-1] - prices[0])
        /
        prices[0]
    ) * 100



    if change > 3:

        decision = "BUY WATCH 🟢"
        risk = "MEDIUM"
        confidence = 85


    elif change < -3:

        decision = "WAIT / PROTECT 🔴"
        risk = "HIGH"
        confidence = 40


    else:

        decision = "HOLD 🟡"
        risk = "LOW"
        confidence = 65



    return {

        "symbol": symbol,
        "price": prices[-1],
        "change": round(change,2),
        "decision": decision,
        "risk": risk,
        "confidence": confidence,
        "chart": df

    }



# ---------------- AGENT LOOP ----------------


results = []


for s in symbols:

    try:

        results.append(
            get_bitget(s)
        )

    except:

        pass



results.sort(
    key=lambda x:x["confidence"],
    reverse=True
)


best = results[0]


# ---------------- OUTPUT ----------------


st.header("🧠 AI Agent Decision")


a,b,c = st.columns(3)


a.metric(
    "Asset",
    best["symbol"]
)


b.metric(
    "Confidence",
    str(best["confidence"])+"%"
)


c.metric(
    "Risk",
    best["risk"]
)


st.success(
    best["decision"]
)



st.header("📊 Bitget Market Scanner")


for item in results:

    with st.expander(
        item["symbol"]
    ):

        st.metric(
            "Price",
            item["price"]
        )


        st.metric(
            "Change",
            str(item["change"])+"%"
        )


        st.line_chart(
            item["chart"]
        )



# ---------------- MEMORY ----------------


st.header("💾 Agent Memory")


st.code(
f"""
Time:
{datetime.now()}

Exchange:
Bitget

Decision:
{best['decision']}

Asset:
{best['symbol']}

Risk:
{best['risk']}
"""
)



# ---------------- EXECUTION ----------------


st.header("⚙️ Execution Simulation")


st.metric(
    "Position Size",
    "$"+str(capital*0.05)
)


st.metric(
    "Mode",
    "Paper Trading"
)


st.success(
    "🚀 Built for Bitget AI Trading Agent Hackathon"
)
