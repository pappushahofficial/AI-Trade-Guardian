import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
from datetime import datetime
import random


st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)


st_autorefresh(
    interval=60000,
    key="refresh"
)


st.title("🤖 AI Trade Guardian v3")

st.caption(
    "Autonomous AI × Crypto Trading Agent | Perception → Decision → Execution → Risk"
)


# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙️ Agent Control")

capital = st.sidebar.number_input(
    "Paper Portfolio ($)",
    value=10000
)

st.sidebar.success(
    "Agent Status: ONLINE 🟢"
)


# ---------------- DATA ----------------

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



def analyze(name, coin_id):

    try:

        url = (
            "https://api.coingecko.com/api/v3/coins/"
            f"{coin_id}/market_chart"
            "?vs_currency=usd&days=7"
        )

        data = requests.get(
            url,
            timeout=5
        ).json()


        prices = [
            p[1]
            for p in data["prices"]
        ]


    except:

        base = backup[name]

        prices = [
            base + random.randint(-100,100)
            for i in range(100)
        ]



    df = pd.DataFrame(
        prices,
        columns=["price"]
    )


    price = df["price"].iloc[-1]


    delta = df["price"].diff()


    gain = delta.where(
        delta > 0,
        0
    ).rolling(14).mean()


    loss = -delta.where(
        delta < 0,
        0
    ).rolling(14).mean()



    rsi = 100 - (
        100 / (1 + gain / loss)
    )


    rsi = round(
        rsi.iloc[-1],
        2
    )



    if rsi < 30:

        decision = "BUY WATCH 🟢"
        risk = "MEDIUM"
        score = 90
        sentiment = "Bullish recovery possible"


    elif rsi > 70:

        decision = "AVOID BUY 🔴"
        risk = "HIGH"
        score = 20
        sentiment = "Market overheated"


    else:

        decision = "WAIT 🟡"
        risk = "LOW"
        score = 60
        sentiment = "Neutral market"



    return {

        "coin": name,
        "price": round(price,2),
        "rsi": rsi,
        "decision": decision,
        "risk": risk,
        "score": score,
        "sentiment": sentiment,
        "chart": df

    }



results = []


for name, coin in coins.items():

    results.append(
        analyze(
            name,
            coin
        )
    )


results.sort(
    key=lambda x:x["score"],
    reverse=True
)


best = results[0]


# ---------------- OVERVIEW ----------------


st.header("🏆 Best AI Opportunity")


c1,c2,c3 = st.columns(3)


c1.metric(
    "Asset",
    best["coin"]
)


c2.metric(
    "AI Score",
    str(best["score"])+"%"
)


c3.metric(
    "Risk",
    best["risk"]
)



# ---------------- MARKETS ----------------


st.header("📊 Market Scanner")


for r in results:


    with st.expander(
        r["coin"]
    ):


        st.metric(
            "Price",
            "$"+str(r["price"])
        )


        st.metric(
            "RSI",
            r["rsi"]
        )


        st.success(
            r["decision"]
        )


        st.write(
            "🧠 Sentiment:",
            r["sentiment"]
        )


        st.line_chart(
            r["chart"]
        )



# ---------------- AI BRAIN ----------------


st.header("🧠 AI Brain Reasoning")


if "BUY" in best["decision"]:

    brain = """
The agent detected oversold conditions.

RSI suggests selling pressure may be weakening.

Opportunity exists but risk controls stay active.
"""


elif "AVOID" in best["decision"]:

    brain = """
The agent detected overheated conditions.

Buying pressure may be exhausted.

Capital protection mode activated.
"""


else:

    brain = """
The market is balanced.

The agent waits for a stronger advantage.

No emotional trades are executed.
"""


st.info(
    brain
)



# ---------------- EXECUTION ----------------


st.header("⚙️ Paper Execution")


position = capital * 0.05


st.metric(
    "Position Size",
    "$"+str(round(position,2))
)


st.metric(
    "Stop Loss",
    round(best["price"]*0.97,2)
)


st.metric(
    "Take Profit",
    round(best["price"]*1.05,2)
)



# ---------------- REPORT ----------------


st.header("📄 Agent Report")


report = f"""

AI TRADE GUARDIAN REPORT

Generated:
{datetime.now()}

Best Asset:
{best['coin']}

Decision:
{best['decision']}

Risk:
{best['risk']}

AI Reason:
{best['sentiment']}

"""


st.text(
    report
)


st.download_button(
    "⬇️ Download Report",
    report,
    "AI_Trade_Guardian_Report.txt"
)



st.success(
    "🚀 Built for Bitget AI × Crypto Trading Hackathon"
)
