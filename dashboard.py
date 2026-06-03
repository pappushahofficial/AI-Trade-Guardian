import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import random
from openai import OpenAI


st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st_autorefresh(
    interval=60000,
    key="refresh"
)


client = OpenAI(
    api_key=st.secrets["QWEN_API_KEY"],
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)


st.title("🤖 AI Trade Guardian v4")

st.caption(
    "Real Qwen Powered Crypto Trading Agent"
)


st.sidebar.title("⚙️ Control")

capital = st.sidebar.number_input(
    "Capital ($)",
    value=10000
)


st.sidebar.success(
    "Qwen Brain Online 🟢"
)



coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana"
}


backup = {
    "Bitcoin": 67000,
    "Ethereum": 3500,
    "Solana": 150
}



def get_market(name, coin):

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


    return {

        "coin": name,

        "price": round(
            df["price"].iloc[-1],
            2
        ),

        "rsi": round(
            rsi.iloc[-1],
            2
        ),

        "chart": df
    }



data = []


for name, coin in coins.items():

    data.append(
        get_market(
            name,
            coin
        )
    )


best = data[0]



def qwen_ai(asset):

    prompt = f"""
You are an AI crypto trading assistant.

Analyze:

Coin: {asset['coin']}
Price: {asset['price']}
RSI: {asset['rsi']}

Give:
Decision
Risk
Reason
"""


    response = client.chat.completions.create(
        model="qwen-plus",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )


    return response.choices[0].message.content



st.header("📊 Market Scanner")


for item in data:

    st.subheader(
        item["coin"]
    )


    st.metric(
        "Price",
        "$" + str(item["price"])
    )


    st.metric(
        "RSI",
        item["rsi"]
    )


    st.line_chart(
        item["chart"]
    )



st.header("🧠 Real Qwen AI Brain")


try:

    result = qwen_ai(best)

    st.success(
        result
    )


except Exception as e:

    st.error(
        "Qwen connection failed"
    )



st.header("🛡 Risk Engine")


st.metric(
    "Position Size",
    "$" + str(capital * 0.05)
)



st.success(
    "🚀 AI Trade Guardian powered by Qwen"
)
