import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import requests
import random
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


st.title("🤖 AI Trade Guardian")

st.caption(
    "Autonomous Crypto Agent | Perception → Decision → Execution → Risk"
)


# CONTROL PANEL

st.sidebar.header("⚙️ Agent Control")

capital = st.sidebar.number_input(
    "Virtual Capital ($)",
    value=10000
)

st.sidebar.success(
    "Agent Running 🟢"
)


# MARKET DATA

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


def scan(name, coin):

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


    change = (
        (df.price.iloc[-1] - df.price.iloc[0])
        /
        df.price.iloc[0]
    ) * 100


    if change > 3:

        decision = "BUY WATCH 🟢"
        risk = "MEDIUM"
        confidence = 85


    elif change < -3:

        decision = "PROTECT / WAIT 🔴"
        risk = "HIGH"
        confidence = 40


    else:

        decision = "HOLD 🟡"
        risk = "LOW"
        confidence = 65


    return {

        "coin": name,
        "price": round(df.price.iloc[-1],2),
        "change": round(change,2),
        "decision": decision,
        "risk": risk,
        "confidence": confidence,
        "chart": df

    }



# AGENT LOOP

results = []

for name, coin in coins.items():

    results.append(
        scan(name,coin)
    )


results.sort(
    key=lambda x:x["confidence"],
    reverse=True
)


best = results[0]



# DECISION

st.header("🧠 AI Agent Decision")


a,b,c = st.columns(3)


a.metric(
    "Selected Asset",
    best["coin"]
)

b.metric(
    "Confidence",
    str(best["confidence"])+"%"
)

c.metric(
    "Risk",
    best["risk"]
)



st.info(
    best["decision"]
)



# SCANNER

st.header("📊 Market Scanner")


for item in results:

    with st.expander(item["coin"]):

        st.metric(
            "Price",
            "$"+str(item["price"])
        )

        st.metric(
            "7D Change",
            str(item["change"])+"%"
        )

        st.line_chart(
            item["chart"]
        )



# MEMORY

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



# EXECUTION

st.header("⚙️ Execution Simulation")


st.metric(
    "Position Size",
    "$"+str(capital*0.05)
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
    "🚀 Ready for Bitget AI Trading Agent Hackathon"
)
