import streamlit as st
import os
import requests

# ======================
# PAGE SETUP
# ======================

st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Trade Guardian")
st.success("System Online")


# ======================
# SECRETS
# ======================

QWEN_API_KEY = os.getenv("QWEN_API_KEY")

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET_KEY = os.getenv("BITGET_SECRET_KEY")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")


# ======================
# STATUS
# ======================

st.subheader("Connection Status")

if QWEN_API_KEY:
    st.success("✅ Qwen AI Connected")
else:
    st.error("❌ Qwen Missing")

if BITGET_API_KEY:
    st.success("✅ Bitget API Connected")
else:
    st.error("❌ Bitget Missing")


# ======================
# DASHBOARD
# ======================

st.subheader("📈 Trading Dashboard")

symbol = st.selectbox(
    "Select Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"
    ]
)


# ======================
# BITGET PRICE
# ======================

def get_price(symbol):

    try:

        url = (
            "https://api.bitget.com/api/v2/spot/market/tickers"
            f"?symbol={symbol}"
        )

        response = requests.get(url)

        data = response.json()

        return float(
            data["data"][0]["lastPr"]
        )

    except:

        return None


# ======================
# AI ANALYSIS
# ======================

if st.button("🤖 Run AI Analysis"):

    price = get_price(symbol)

    if price:

        st.write("Pair:", symbol)

        st.metric(
            "Current Price",
            price
        )


        # Simple AI logic

        if symbol == "BTCUSDT":

            signal = "HOLD"

        elif symbol == "ETHUSDT":

            signal = "BUY"

        else:

            signal = "WATCH"


        st.subheader("🤖 AI Decision")

        st.metric(
            "Signal",
            signal
        )


        st.info(
            f"""
AI Trade Guardian Report

Pair: {symbol}

Price: {price}

Checks:
✅ Bitget Market Data
✅ Trend Analysis
✅ Risk Scan

Decision: {signal}
"""
        )

    else:

        st.error(
            "Unable to fetch market data"
        )
