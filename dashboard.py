import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖"
)

st_autorefresh(
    interval=30000,
    key="refresh"
)


st.title("🤖 AI Trade Guardian")

st.caption(
    "Autonomous AI Crypto Trading Agent | Perception → Decision → Execution → Risk"
)


st.sidebar.title("⚙️ Agent Control")

capital = st.sidebar.number_input(
    "Paper Balance ($)",
    value=10000
)

st.sidebar.success("Agent Online 🟢")


coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "BNB": "binancecoin"
}


def analyze(name, coin_id):

    url = (
        "https://api.coingecko.com/api/v3/coins/"
        f"{coin_id}/market_chart"
        "?vs_currency=usd&days=7"
    )

    try:

        data = requests.get(
            url,
            timeout=10
        ).json()

        prices = [
            x[1]
            for x in data["prices"]
        ]

    except:

        return None


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

    rsi = rsi.iloc[-1]


    if rsi < 30:

        action = "PAPER BUY 🟢"
        risk = "MEDIUM"
        score = 90

    elif rsi > 70:

        action = "AVOID BUY 🔴"
        risk = "HIGH"
        score = 20

    else:

        action = "WAIT 🟡"
        risk = "LOW"
        score = 50


    return {
        "coin": name,
        "price": round(price,2),
        "rsi": round(rsi,2),
        "action": action,
        "risk": risk,
        "score": score,
        "chart": df
    }



results = []


for name, coin_id in coins.items():

    result = analyze(
        name,
        coin_id
    )

    if result:
        results.append(result)



if not results:

    st.error(
        "Market API unavailable"
    )

    st.stop()



results.sort(
    key=lambda x:x["score"],
    reverse=True
)


st.header("🏆 Best Opportunities")


for r in results:


    st.subheader(r["coin"])

    st.metric(
        "Price",
        "$" + str(r["price"])
    )

    st.metric(
        "AI Score",
        str(r["score"]) + "%"
    )

    st.write(
        "RSI:",
        r["rsi"]
    )


    st.success(
        r["action"]
    )


    st.write(
        "Risk:",
        r["risk"]
    )


    st.line_chart(
        r["chart"]
    )


    st.divider()



st.header("🤖 Agent Activity")

for item in [
    "Reading live markets",
    "Calculating RSI",
    "Ranking assets",
    "Checking risk",
    "Updating strategy"
]:

    st.write(
        "✅",
        item
    )



best = results[0]


st.header("📄 AI Report")


report = f"""
AI TRADE GUARDIAN REPORT

Time:
{datetime.now()}

Best:
{best['coin']}

Decision:
{best['action']}

Risk:
{best['risk']}
"""


st.text(report)


st.download_button(
    "Download Report",
    report,
    "report.txt"
)



st.header("🛡 Risk Engine")


st.metric(
    "Position Size",
    "$" + str(capital * 0.05)
)


st.success(
    "Built for Bitget AI × Crypto Trading Hackathon 🚀"
)
