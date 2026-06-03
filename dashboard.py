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


# Sidebar

st.sidebar.title("⚙️ Agent Control")

capital = st.sidebar.number_input(
    "Paper Balance ($)",
    value=10000
)

st.sidebar.success(
    "Agent Online 🟢"
)


coins = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT"
]


def analyze(symbol):

    url = (
        "https://api.binance.com/api/v3/klines"
        f"?symbol={symbol}&interval=1h&limit=100"
    )


    try:

        data = requests.get(
            url,
            timeout=10
        ).json()


        if not data or "code" in data:
            return None


        prices = [
            float(c[4])
            for c in data
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
        "coin": symbol,
        "price": price,
        "rsi": round(rsi,2),
        "action": action,
        "risk": risk,
        "score": score,
        "chart": df
    }



results = []


for coin in coins:

    result = analyze(coin)

    if result:
        results.append(
            result
        )



if len(results) == 0:

    st.error(
        "Market API unavailable. Try again later."
    )

    st.stop()



results.sort(
    key=lambda x: x["score"],
    reverse=True
)



st.header("🏆 Best Opportunities")


for r in results:


    st.subheader(
        r["coin"]
    )


    st.metric(
        "Price",
        r["price"]
    )


    st.metric(
        "Score",
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


    if "BUY" in r["action"]:

        with open(
            "paper_trades.txt",
            "a",
            encoding="utf-8"
        ) as file:


            file.write(
                f"{datetime.now()} | {r['coin']} | PAPER BUY\n"
            )


        st.info(
            "Paper Trade Executed ✅"
        )


    st.line_chart(
        r["chart"]
    )


    st.divider()



st.header("📜 Agent Memory")


try:

    history = open(
        "paper_trades.txt",
        encoding="utf-8"
    ).read()


    st.text(
        history
    )


except:

    st.write(
        "No trades yet"
    )




st.header("🤖 Agent Activity Monitor")


activities = [
    "📡 Fetching market data",
    "📊 Calculating RSI",
    "🏆 Ranking opportunities",
    "🛡️ Checking risk",
    "⚙️ Managing execution",
    "💾 Updating memory"
]


for a in activities:

    st.write(
        "✅",
        a
    )




best = results[0]


st.header("📄 AI Market Report")


report = f"""

🤖 AI TRADE GUARDIAN REPORT

Generated:
{datetime.now()}

Best Opportunity:
{best['coin']}

Price:
{best['price']}

RSI:
{best['rsi']}

Decision:
{best['action']}

Risk:
{best['risk']}

"""


st.text(report)


st.download_button(
    "⬇️ Download Report",
    report,
    "AI_Trade_Report.txt"
)




st.header("🛡️ Risk Management")


position = capital * 0.05


st.metric(
    "Position Size",
    "$" + str(round(position,2))
)


st.metric(
    "Stop Loss",
    round(best["price"] * 0.97,2)
)


st.metric(
    "Take Profit",
    round(best["price"] * 1.05,2)
)



st.success(
    "Built for Bitget AI × Crypto Trading Hackathon 🚀"
)
