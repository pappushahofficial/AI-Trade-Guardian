import os
import requests
import pandas as pd
from datetime import datetime
import time

# ======================
# API SECRETS
# ======================

QWEN_API_KEY = os.getenv("QWEN_API_KEY")

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET_KEY = os.getenv("BITGET_SECRET_KEY")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")


# ======================
# APP START
# ======================

print("AI Trade Guardian ONLINE")


# Check secrets loaded
if BITGET_API_KEY:
    print("Bitget API Connected")
else:
    print("Bitget API Missing")


if QWEN_API_KEY:
    print("Qwen AI Connected")
else:
    print("Qwen API Missing")


# ======================
# RSI FUNCTION
# ======================

def calculate_rsi(prices, period=14):
    delta = prices.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# ======================
# MAIN LOOP
# ======================

while True:
    print("AI Trade Guardian Running...")
    time.sleep(60)
