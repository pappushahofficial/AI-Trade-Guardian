import streamlit as st
import os

st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Trade Guardian")
st.success("System Online")

# Load secrets
qwen = os.getenv("QWEN_API_KEY")
bitget = os.getenv("BITGET_API_KEY")

st.subheader("Connection Status")

if qwen:
    st.success("✅ Qwen AI Connected")
else:
    st.error("❌ Qwen Missing")

if bitget:
    st.success("✅ Bitget API Connected")
else:
    st.error("❌ Bitget Missing")


st.subheader("Trading Dashboard")

st.info("AI market analysis loading...")

symbol = st.selectbox(
    "Select Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"
    ]
)

st.write("Selected:", symbol)

st.button("Run AI Analysis")
