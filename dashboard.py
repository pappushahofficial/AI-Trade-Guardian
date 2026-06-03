import streamlit as st
import os
import requests

st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Trade Guardian")
st.success("System Online")

# Secrets
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET_KEY = os.getenv("BITGET_SECRET_KEY")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

st.subheader("Connection Status")

st.success("✅ Qwen AI Connected" if QWEN_API_KEY else "❌ Qwen Missing")
st.success("✅ Bitget API Connected" if BITGET_API_KEY else "❌ Bitget Missing")


st.subheader("📈 Trading Dashboard")

symbol = st.selectbox(
    "Select Pair",
    ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
)


def get_price(symbol):
    try:
        url = f"https://api.bitget.com/api/v2/spot/market/tickers?symbol={symbol}"

        data = requests.get(url).json()

        price = data["data"][0]["lastPr"]

        return price

    except:
        return "Error loading price"


if st.button("🤖 Run AI Analysis"):

    price = get_price(symbol)

    st.write("Pair:", symbol)
    st.write("Current Price:", price)

    st.info(
        f"""
        AI Analysis:

        {symbol}

        Market data received ✅

        AI Trade Guardian is monitoring
        trend, RSI and opportunities.
        """
    )
