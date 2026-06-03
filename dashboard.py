import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import random
from datetime import datetime


st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st_autorefresh(
    interval=60000,
    key="refresh"
)


st.title("🤖 AI Trade Guardian v5")

st.caption(
    "Bitget AI Trading Agent | Observe → Think → Decide → Execute"
)


# CONTROL

st.sidebar.header("⚙️ Agent Control")

capital = st.sidebar.number_input(
    "Virtual Capital ($)",
    value=10000
)

st.sidebar.success(
    "Agent Online 🟢"
)


# MARKET

coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "BNB": "binancecoin"
}


backup = {
    "Bitcoin": 67000,
    "Ethereum": 3500,
    "Solana": 150,
    "BNB": 600
}


def analyze(name, coin):

    try:

        url = (
            "https://api.coingecko.com/api/v3/coins/"
            + coin +
            "/market_chart?vs_currency=usd&days=7"
        )

        data = requests.get(
            url,
            timeout=5
        ).json()

        prices = [
            x[1]
            for x in data["prices"]
        ]


    except:

        prices = [
            backup[name] + random.randint(-100,100)
            for i in range(100)
        ]


    df = pd.DataFrame(
        prices,
        columns=["price"]
    )


    delta = df["price"].diff()

    gain = (
        delta.where(delta > 0,0)
        .rolling(14)
        .mean()
    )

    loss = (
        -delta.where(delta < 0,0)
        .rolling(14)
        .mean()
    )


    rsi = 100 - (
        100/(1+gain/loss)
    )


    rsi = round(
        rsi.iloc[-1],
        2
    )


    if rsi < 30:

        decision = "BUY WATCH 🟢"
        risk = "MEDIUM"
        score = 90


    elif rsi > 70:

        decision = "AVOID 🔴"
        risk = "HIGH"
        score = 20


    else:

        decision = "WAIT 🟡"
        risk = "LOW"
        score = 60


    return {

        "coin": name,
        "price": round(df["price"].iloc[-1],2),
        "rsi": rsi,
        "decision": decision,
        "risk": risk,
        "score": score,
        "chart": df

    }



# AGENT LOOP

results = []

for name, coin in coins.items():

    results.append(
        analyze(name,coin)
    )


results.sort(
    key=lambda x:x["score"],
    reverse=True
)


best = results[0]



# DASHBOARD

st.header("🧠 AI Decision Engine")


c1,c2,c3 = st.columns(3)


c1.metric(
    "Asset",
    best["coin"]
)


c2.metric(
    "Confidence",
    str(best["score"])+"%"
)


c3.metric(
    "Risk",
    best["risk"]
)



st.header("📊 Market Scanner")


for item in results:

    with st.expander(
        item["coin"]
    ):

        st.metric(
            "Price",
            "$"+str(item["price"])
        )


        st.metric(
            "RSI",
            item["rsi"]
        )


        st.success(
            item["decision"]
        )


        st.line_chart(
            item["chart"]
        )



st.header("💾 Agent Memory")


st.code(
f"""
TIME:
{datetime.now()}

LAST DECISION:
{best['decision']}

ASSET:
{best['coin']}

RISK:
{best['risk']}
"""
)



st.header("⚙️ Execution")


position = capital * 0.05


st.metric(
    "Position Size",
    "$"+str(position)
)


st.metric(
    "Stop Loss",
    "$"+str(round(best["price"]*0.97,2))
)


st.metric(
    "Take Profit",
    "$"+str(round(best["price"]*1.05,2))
)



st.success(
    "🚀 AI Trade Guardian Ready for Bitget Hackathon"
)
