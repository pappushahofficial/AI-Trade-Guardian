import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import random
from datetime import datetime
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


# REAL QWEN BRAIN

client = OpenAI(
    api_key=st.secrets["QWEN_API_KEY"],
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)


st.title("🤖 AI Trade Guardian v4")

st.caption(
    "Real Qwen Powered Autonomous Crypto Trading Agent 🧠"
)


st.sidebar.title("⚙️ Control")

capital = st.sidebar.number_input(
    "Capital ($)",
    value=10000
)

st.sidebar.success(
    "Qwen Brain Online 🧠🟢"
)


coins = {
    "Bitcoin":"bitcoin",
    "Ethereum":"ethereum",
    "Solana":"solana",
    "BNB":"binancecoin"
}


backup = {
    "Bitcoin":67000,
    "Ethereum":3500,
    "Solana":150,
    "BNB":600
}



def analyze(name, coin):

    try:

        url = (
            "https://api.coingecko.com/api/v3/coins/"
            f"{coin}/market_chart?vs_currency=usd&days=7"
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


    price = df.price.iloc[-1]

    delta = df.price.diff()


    gain = delta.where(
        delta > 0,
        0
    ).rolling(14).mean()


    loss = -delta.where(
        delta < 0,
        0
    ).rolling(14).mean()


    rsi = 100 - (
        100/(1+gain/loss)
    )

    rsi = round(
        rsi.iloc[-1],
        2
    )


    return {
        "coin":name,
        "price":round(price,2),
        "rsi":rsi,
        "chart":df
    }



results=[]


for n,c in coins.items():

    results.append(
        analyze(n,c)
    )


best = results[0]


# QWEN THINKING

def qwen_brain(asset):

    prompt = f"""

You are an autonomous crypto trading AI.

Analyze:

Coin:
{asset['coin']}

Price:
{asset['price']}

RSI:
{asset['rsi']}

Give:
- Market condition
- Buy/wait decision
- Risk level
- Reason

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



st.header("
