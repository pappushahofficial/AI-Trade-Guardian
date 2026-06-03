import requests
import pandas as pd
from datetime import datetime
import time

print("🤖 AI Trade Guardian ONLINE")

def calculate_rsi(prices, period=14):
    delta = prices.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()

    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]


def analyze_market():

    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

    data = requests.get(url).json()

    prices = []

    for candle in data:
        prices.append(float(candle[4]))

    df = pd.DataFrame(prices, columns=["price"])

    current_price = df["price"].iloc[-1]
    average_price = df["price"].mean()
    rsi = calculate_rsi(df["price"])

    if rsi < 30:
        decision = "BUY WATCH"
        risk = "MEDIUM"
        reason = "RSI shows oversold market"

    elif rsi > 70:
        decision = "SELL / AVOID BUY"
        risk = "HIGH"
        reason = "RSI shows overbought market"

    else:
        decision = "WAIT"
        risk = "LOW"
        reason = "Market is neutral"

    print("----------------")
    print("Time:", datetime.now())
    print("BTC:", current_price)
    print("Average:", round(average_price, 2))
    print("RSI:", round(rsi, 2))

    print("Decision:", decision)
    print("Risk:", risk)
    print("Reason:", reason)

    with open("trade_history.txt", "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now()} | BTC {current_price} | RSI {round(rsi,2)} | {decision}\n"
        )

    print("Memory Updated ✅")


while True:
    analyze_market()
    print("Sleeping 30 seconds...\n")
    time.sleep(30)