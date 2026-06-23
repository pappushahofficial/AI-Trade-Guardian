import streamlit as st
import os
import requests
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI
from datetime import datetime
import sqlite3
import xml.etree.ElementTree as ET
import json

# =========================
# AGENT TRADE DATABASE
# =========================

conn = sqlite3.connect("trade_logs.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    asset TEXT,
    decision TEXT,
    entry TEXT,
    stop_loss TEXT,
    take_profit TEXT,
    confidence TEXT,
    reasoning TEXT
)
""")

conn.commit()

# Migration safety: add reasoning column if an older DB file already exists without it
cursor.execute("PRAGMA table_info(trades)")
_existing_cols = [row[1] for row in cursor.fetchall()]
if "reasoning" not in _existing_cols:
    cursor.execute("ALTER TABLE trades ADD COLUMN reasoning TEXT")
    conn.commit()


def save_trade_log(asset, decision, entry, stop_loss, take_profit, confidence, reasoning=""):
    cursor.execute(
        """
        INSERT INTO trades
        (time, asset, decision, entry, stop_loss, take_profit, confidence, reasoning)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            asset,
            decision,
            entry,
            stop_loss,
            take_profit,
            confidence,
            reasoning
        )
    )
    conn.commit()


def load_trade_logs():
    cursor.execute(
        "SELECT time, asset, decision, entry, stop_loss, take_profit, confidence, reasoning FROM trades"
    )
    return cursor.fetchall()


def load_recent_decisions(asset=None, limit=5):
    """Pull the agent's most recent past decisions for memory context, optionally filtered by asset."""
    if asset:
        cursor.execute(
            """
            SELECT time, asset, decision, confidence, reasoning FROM trades
            WHERE asset = ?
            ORDER BY id DESC LIMIT ?
            """,
            (asset, limit)
        )
    else:
        cursor.execute(
            "SELECT time, asset, decision, confidence, reasoning FROM trades ORDER BY id DESC LIMIT ?",
            (limit,)
        )
    return cursor.fetchall()

if "trade_logs" not in st.session_state:
    st.session_state.trade_logs = []

if "agent_start_time" not in st.session_state:
    st.session_state.agent_start_time = datetime.now()


def get_uptime_str():
    delta = datetime.now() - st.session_state.agent_start_time
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

st.set_page_config(
    page_title="AI Trade Guardian",
    page_icon="🤖",
    layout="wide"
)

# ======================
# PRO DARK DASHBOARD UI
# ======================


st.markdown(
"""
<style>

.stApp {
    background:#050816;
    color:white;
}


.block-container {
    padding-top:2rem;
}


section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #050816,
    #0f172a
    );

}


h1,h2,h3 {
    color:white;
}


.card {

    background:#0f172a;

    padding:25px;

    border-radius:25px;

    border:1px solid #1e293b;

    box-shadow:
    0 0 25px #020617;

}


.neon {

    color:#22d3ee;

}


.stButton button {

    height:60px;

    width:100%;

    border-radius:20px;

    background:
    linear-gradient(
    90deg,
    #06b6d4,
    #9333ea
    );

    color:white;

    font-size:22px;

    border:none;

}


[data-testid="stMetric"] {

    background:#0f172a;

    padding:20px;

    border-radius:20px;

    border:1px solid #334155;

}


.stTextInput input {

    background:#020617;

    color:white;

    border-radius:15px;

}


</style>
""",
unsafe_allow_html=True
)



# ======================
# SIDEBAR
# ======================


with st.sidebar:


    st.markdown(
    """
<div style="text-align:center">

<div style="
font-size:65px;
width:90px;
height:90px;
margin:auto;
display:flex;
align-items:center;
justify-content:center;
background:#111827;
border-radius:25px;
border:2px solid #22d3ee;
box-shadow:0 0 30px #06b6d4;
margin-bottom:15px;
">
🤖
</div>

<h2>AI Trade<br>Guardian</h2>

<p style="color:#94a3b8">
Autonomous Trading Agent
</p>

</div>
""",
    unsafe_allow_html=True
    )


    st.success("🟢 Online")


    st.markdown("---")


    # ======================
# CLICKABLE MENU
# ======================

menu = st.sidebar.radio(
    "Menu",
    [
        "📈 Market Scanner",
        "⭐ Watchlist",
        "ℹ️ About Agent",
        "⚙️ Settings",
        "📊 Trade Logs"
    ]
)


# ======================
# SETTINGS PAGE
# ======================

if menu == "⚙️ Settings":

    st.sidebar.markdown("---")

    dark_mode = st.sidebar.toggle(
        "🌙 Dark Mode",
        value=True
    )

    if dark_mode:

        st.sidebar.success(
            "Dark Theme Active"
        )

    else:

        st.sidebar.info(
            "Light Theme Active"
        )

# =========================
# TRADE LOGS PAGE
# =========================

elif menu == "ℹ️ About Agent":

    st.title("🤖 About AI Trade Guardian")

    st.markdown("""
## Autonomous Crypto Trading Agent 🚀

Powered by Alibaba Qwen AI + Bitget API

AI Trade Guardian is an AI-powered trading assistant that analyzes live crypto markets, applies AI reasoning, manages risk, and creates structured trading decisions.

---

### 🤖 Agent Workflow

📊 Perceive  
⬇️  
🧠 Analyze  
⬇️  
🎯 Decide  
⬇️  
⚡ Execute  
⬇️  
🧾 Remember  

---

### ✨ Features

✅ Live Bitget Market Data  
✅ Alibaba Qwen AI Integration  
✅ Market Scanner  
✅ RSI, EMA, Volatility & Volume Analysis  
✅ Live Crypto News (CoinDesk + CoinTelegraph)  
✅ Crypto Fear & Greed Index  
✅ AI-Driven LONG / SHORT / WAIT Decisions  
✅ Dynamic Confidence Score  
✅ Stop Loss & Take Profit Planning  
✅ Virtual Execution Center  
✅ Persistent Agent Memory with Reasoning  
✅ Trade Logs  

---

### 👨‍💻 Developer

Created by **Pappu Shah DMC Developer**

🔗 Telegram: https://t.me/PappuShahOfficial  
💻 GitHub: https://github.com/pappushahofficial

🏆 Built for Bitget AI Hackathon
""")

elif menu == "📊 Trade Logs":

    st.subheader("📊 Agent Trade Logs")

    logs = load_trade_logs()

    if len(logs) == 0:
        st.info("No trades executed yet")
    else:
        logs = pd.DataFrame(
            logs,
            columns=[
                "Time",
                "Asset",
                "Decision",
                "Entry",
                "Stop Loss",
                "Take Profit",
                "Confidence",
                "Reasoning"
            ]
        )

        st.dataframe(
            logs,
            use_container_width=True
        )
    # ======================
# AGENT STATUS
# ======================

st.sidebar.markdown("---")

_all_logs = load_trade_logs()
_signal_count = len(_all_logs)
_last_confidence = _all_logs[-1][6] if _signal_count > 0 else "—"
_uptime_str = get_uptime_str()

st.sidebar.markdown(
f"""
<div class="card">

<h4>🤖 AGENT STATUS</h4>

<p>🟢 <b>Status:</b> Online</p>

<p>⏱ <b>Uptime:</b> {_uptime_str}</p>

<p>📊 <b>Signals Generated:</b> {_signal_count}</p>

<p>🎯 <b>Last Confidence:</b> {_last_confidence}</p>

</div>
""",
unsafe_allow_html=True
)


# ======================
# POWERED BY
# ======================

st.sidebar.markdown("---")

st.sidebar.markdown(
"""
<div class="card">

<h4>POWERED BY</h4>

<p>🧠 Alibaba Qwen AI</p>

<p>📡 Bitget API</p>

<p>📰 CoinDesk / CoinTelegraph</p>

<p>😨 Alternative.me F&G Index</p>

</div>
""",
unsafe_allow_html=True
)
def get_data(coin_symbol=None):


    url = (
        "https://api.bitget.com/api/v2/spot/market/candles"
        f"?symbol={coin_symbol if coin_symbol else 'BTCUSDT'}&granularity=15min&limit=100"
    )


    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception:
        # Network error or bad response - treat as invalid pair
        return None


    # Bitget returns an empty/missing "data" list for invalid symbols
    candles = data.get("data") if isinstance(data, dict) else None

    if not candles:
        return None


    df = pd.DataFrame(candles)


    # Safety check: a valid candle response always has at least 6 columns
    if df.shape[1] < 6:
        return None


    df = df.iloc[:, :6]


    df.columns = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]


    df["close"] = (
        df["close"]
        .astype(float)
    )

    # volume is the 6th candle field returned by Bitget
    df["volume"] = (
        df["volume"]
        .astype(float)
    )

    return df


def add_indicators(df):
    """Adds RSI, volatility, volume trend, and momentum columns to a candle dataframe."""

    df["EMA20"] = df["close"].ewm(span=20).mean()
    df["EMA50"] = df["close"].ewm(span=50).mean()

    # RSI (14-period, Wilder smoothing)
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / 14, min_periods=14).mean()
    avg_loss = loss.ewm(alpha=1 / 14, min_periods=14).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-9)
    df["RSI"] = 100 - (100 / (1 + rs))
    df["RSI"] = df["RSI"].fillna(50)

    # Volatility: rolling std dev of % returns over last 20 candles, annualized-style scale for readability
    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(window=20).std() * 100
    df["volatility"] = df["volatility"].fillna(0)

    # Volume trend: current volume vs its own 20-period average
    df["volume_avg20"] = df["volume"].rolling(window=20).mean()
    df["volume_avg20"] = df["volume_avg20"].fillna(df["volume"])

    return df


def get_fear_greed_index():
    """Fetches the current crypto Fear & Greed Index from Alternative.me. Returns (value, label) or (None, None)."""

    try:
        response = requests.get(
            "https://api.alternative.me/fng/?limit=1",
            timeout=8
        )
        data = response.json()
        entry = data.get("data", [None])[0]

        if not entry:
            return None, None

        return int(entry.get("value")), entry.get("value_classification")

    except Exception:
        return None, None


def _strip_html(raw_html):
    """Very small HTML tag stripper for RSS descriptions, no external deps."""
    import re
    return re.sub(r"<[^>]+>", "", raw_html or "").strip()


def get_crypto_news(asset_keywords, max_items=5):
    """
    Fetches recent headlines from CoinDesk and CoinTelegraph RSS feeds,
    filtered to ones mentioning the asset (by symbol or common name keywords).
    Returns a list of headline strings. Headlines only - no full article scraping.
    """

    feeds = [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss"
    ]

    headlines = []

    for feed_url in feeds:
        try:
            resp = requests.get(feed_url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                continue

            root = ET.fromstring(resp.content)

            for item in root.findall(".//item"):
                title_el = item.find("title")
                title = title_el.text.strip() if title_el is not None and title_el.text else ""

                if not title:
                    continue

                title_lower = title.lower()

                if any(kw.lower() in title_lower for kw in asset_keywords):
                    headlines.append(title)

        except Exception:
            continue

    # De-dupe while preserving order, cap to max_items
    seen = set()
    unique_headlines = []
    for h in headlines:
        if h not in seen:
            seen.add(h)
            unique_headlines.append(h)

    return unique_headlines[:max_items]


# Maps a Bitget trading pair to keywords useful for matching news headlines
def get_asset_keywords(symbol):
    base = symbol.upper().replace("USDT", "").replace("USD", "")

    name_map = {
        "BTC": ["BTC", "Bitcoin"],
        "ETH": ["ETH", "Ethereum"],
        "SOL": ["SOL", "Solana"],
        "BGB": ["BGB", "Bitget"],
        "BNB": ["BNB", "Binance Coin"],
        "XRP": ["XRP", "Ripple"],
        "DOGE": ["DOGE", "Dogecoin"],
        "ADA": ["ADA", "Cardano"],
        "AVAX": ["AVAX", "Avalanche"],
        "LINK": ["LINK", "Chainlink"]
    }

    return name_map.get(base, [base])

# ======================
# WATCHLIST PAGE
# ======================

if menu == "⭐ Watchlist":

    st.title("⭐ Watchlist")


    watchlist = [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
        "BGBUSDT"
    ]


    st.markdown(
        """
        <div class="card">

        <h2>🔥 Tracked Assets</h2>

        </div>
        """,
        unsafe_allow_html=True
    )


    for coin in watchlist:


        col1, col2, col3 = st.columns(
            [2,2,1]
        )


        with col1:

            st.write(
                "🟢",
                coin
            )


        with col2:

            st.write(
                "💰 Live Price"
            )


        with col3:

            open_chart = st.button(
                "📈 Chart",
                key=f"chart_{coin}"
            )


        if open_chart:


            st.subheader(
                f"📈 {coin} Live Chart"
            )


            try:


                df = get_data(coin)


                if df is not None:


                    fig = go.Figure(
                        data=[
                            go.Candlestick(

                                x=df["time"],

                                open=df["open"],

                                high=df["high"],

                                low=df["low"],

                                close=df["close"]

                            )
                        ]
                    )


                    fig.update_layout(

                        height=450,

                        xaxis_rangeslider_visible=False

                    )


                    st.plotly_chart(

                        fig,

                        use_container_width=True

                    )


                else:


                    st.error(
                        "❌ No Bitget data"
                    )


            except Exception as e:


                st.error(
                    str(e)
                )



    st.markdown("---")


    st.markdown(
        """
        <div class="card">

        <h3>🤖 AI Watchlist Monitor</h3>

        🧠 Alibaba Qwen AI: Connected

        <br><br>

        📡 Bitget API: Live Data

        <br><br>

        ⚡ Monitoring opportunities

        </div>
        """,
        unsafe_allow_html=True
    )

if menu != "📈 Market Scanner":
    st.stop()

# 📈 Market Scanner Page

# ======================
# HEADER
# ======================

st.title(
    "🤖 Autonomous Crypto Trading Agent 🚀"
)

st.markdown(
    """
### Powered by

🧠 **Alibaba Qwen AI**  |  🔗 **Bitget API**

🏆 Bitget AI Hackathon

📊 Perceive → 🧠 Decide → ⚡ Execute → 🛡 Manage Risk
    """,
    unsafe_allow_html=True
)
st.success(
    "🟢 Trading Agent Online"
)

demo = st.toggle(
    "🧪 Demo Mode (Save Qwen Credits)",
    value=True
)

# =====================
    # CONNECTIONS
    # =====================

st.subheader(
        "🔗 Live Connections"
    )

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "🧠 AI Model",
    "Qwen 3.5",
    "Connected"
)

c2.metric(
    "📈 Market Data",
    "Bitget API",
    "Connected"
)

c3.metric(
    "🤖 Agent",
    "Active",
    "Running"
)

c4.metric(
    "🟢 Status",
    "Live",
    "Ready"
)
# ======================
# API
# ======================

QWEN_API_KEY = os.getenv(
    "BITGET_QWEN_API_KEY"
)


client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://hackathon.bitgetops.com/v1"
)



# ======================
# MARKET SCANNER
# ======================


st.subheader(
    "📈 Market Scanner"
)


default_coin = st.selectbox(
    "🔥 Top Crypto Assets",
    [
        "BTCUSDT",
        "ETHUSDT",
        "BGBUSDT",
        "SOLUSDT",
        "BNBUSDT",
        "XRPUSDT",
        "DOGEUSDT",
        "ADAUSDT",
        "AVAXUSDT",
        "LINKUSDT"
    ]
)


custom_coin = st.text_input(
    "🔎 Custom Bitget Pair",
    placeholder="Example: SUIUSDT"
)


symbol = (
    custom_coin.upper().strip()
    if custom_coin
    else default_coin
)







if st.button(
    "🤖 Launch AI Agent"
):

    with st.spinner(
        "🤖 AI Trade Guardian analyzing market..."
    ):

        df = get_data(symbol)

        if df is None:
            st.error(
                f"❌ Couldn't find data for **{symbol}**. "
                "Please check the pair name and try again (e.g. BTCUSDT, ETHUSDT)."
            )
            st.stop()

        df = add_indicators(df)

        price = df["close"].iloc[-1]

        # =====================
        # FIX 12 - MARKET ANALYSIS SUITE
        # =====================

        ema20 = df["EMA20"].iloc[-1]
        ema50 = df["EMA50"].iloc[-1]
        rsi = df["RSI"].iloc[-1]
        volatility = df["volatility"].iloc[-1]
        current_volume = df["volume"].iloc[-1]
        avg_volume = df["volume_avg20"].iloc[-1]
        volume_trend = (
            "Above Average" if current_volume > avg_volume else "Below Average"
        )

        # EMA separation, normalized against price so it's comparable across assets
        ema_gap_pct = abs(ema20 - ema50) / price * 100

        # Momentum over the last 5 candles
        momentum = (
            (price - df["close"].iloc[-5])
            / df["close"].iloc[-5]
        ) * 100

        # Candle strength (most recent candle move)
        candle_power = abs(
            df["close"].iloc[-1]
            -
            df["close"].iloc[-2]
        ) / price * 100

        # Combined "edge" strength - how convinced the TECHNICAL read is, regardless of direction
        edge_strength = (ema_gap_pct * 4) + (abs(momentum) * 3) + (candle_power * 5)

        # WAIT zone: trend + momentum + candle are all too weak to trust a side
        if ema_gap_pct < 0.05 and abs(momentum) < 0.05:
            technical_direction = "WAIT"
            technical_confidence = 50
        else:
            technical_direction = "LONG" if ema20 > ema50 else "SHORT"
            technical_confidence = 70 + min(15, round(edge_strength))

        # =====================
        # FIX 12 - NEWS + FEAR/GREED
        # =====================

        asset_keywords = get_asset_keywords(symbol)
        news_headlines = get_crypto_news(asset_keywords, max_items=5)
        fng_value, fng_label = get_fear_greed_index()

        # =====================
        # FIX 12 - AGENT MEMORY (past decisions for this asset)
        # =====================

        past_decisions = load_recent_decisions(asset=symbol, limit=3)

        if past_decisions:
            memory_lines = []
            for p_time, p_asset, p_decision, p_confidence, p_reasoning in past_decisions:
                short_reason = (p_reasoning or "")[:120]
                memory_lines.append(
                    f"- {p_time}: {p_decision} ({p_confidence}) — {short_reason}"
                )
            memory_context = "\n".join(memory_lines)
        else:
            memory_context = "No prior decisions recorded for this asset yet."

        # =====================
        # FIX 12 - BUILD QWEN PROMPT (Qwen makes the FINAL call)
        # =====================

        news_block = (
            "\n".join(f"- {h}" for h in news_headlines)
            if news_headlines
            else "No recent relevant headlines found."
        )

        fng_block = (
            f"{fng_value}/100 ({fng_label})"
            if fng_value is not None
            else "Unavailable"
        )

        agent_prompt = f"""
You are an autonomous crypto trading agent. You receive technical indicators,
recent news headlines, the Fear & Greed Index, and your own past decisions for
this asset. You make the FINAL trading decision - you are not required to
agree with the technical-only suggestion below; use it as one input among several.

ASSET: {symbol}
CURRENT PRICE: {price}

TECHNICAL INDICATORS:
- EMA20: {round(ema20, 4)}
- EMA50: {round(ema50, 4)}
- RSI(14): {round(rsi, 1)}
- Volatility (20-candle, % stdev of returns): {round(volatility, 3)}
- Volume: {round(current_volume, 2)} ({volume_trend} vs 20-period avg of {round(avg_volume, 2)})
- Momentum (5-candle % change): {round(momentum, 3)}%
- Technical-only suggested direction: {technical_direction} (suggested confidence {technical_confidence}%)

RECENT NEWS HEADLINES (CoinDesk / CoinTelegraph):
{news_block}

CRYPTO FEAR & GREED INDEX: {fng_block}

YOUR PAST DECISIONS ON {symbol}:
{memory_context}

TASK:
Decide the final trading direction: LONG, SHORT, or WAIT.
Weigh the technical indicators, news sentiment (bullish/bearish/neutral), market
emotion (Fear & Greed), and consistency with your past reasoning on this asset.
RSI above 70 suggests overbought, below 30 suggests oversold. High volatility
means wider risk. Extreme Fear or Extreme Greed often signal potential reversals.

Then produce a detailed trading report a serious trader could act on - concrete
price levels, not vague advice. Use the entry price, stop loss, and take profit
implied by your direction (LONG: SL -2%/TP +4% from entry; SHORT: SL +2%/TP -4%
from entry; WAIT: SL -1%/TP +1%) to compute real numbers for every price level
you mention below - never use placeholders.

Respond with ONLY valid JSON, no markdown formatting, no backticks, no preamble,
matching this exact schema:
{{
  "direction": "LONG" | "SHORT" | "WAIT",
  "confidence": <integer 50-95>,
  "reasoning": "<2-4 sentences - a short summary used for the agent's own memory
   of this trade. Keep this concise.>",

  "summary": "<1-2 sentence systematic summary of the setup, e.g. 'Here's a
   breakdown of your {symbol} {{direction}} setup based on current conditions.'>",

  "trade_metrics": {{
    "risk_reward_ratio": "<e.g. '1 : 2.00'>",
    "risk_reward_note": "<short note, e.g. 'Mathematically optimal for consistent edge'>",
    "breakeven_win_rate": "<e.g. '33.33%'>",
    "breakeven_note": "<short note, e.g. 'Profitable if actual win rate >33.3%'>",
    "risk_per_unit": "<e.g. '2.00%'>",
    "risk_per_unit_note": "<short note, e.g. 'Disciplined; aligns with standard swing/position sizing'>"
  }},

  "structural_analysis": [
    {{"title": "Invalidation Zone", "detail": "<specific price/level and what breaks the thesis if crossed>"}},
    {{"title": "Profit Target Proximity", "detail": "<specific price/level and nearby support/resistance context>"}},
    {{"title": "Leverage vs. Liquidation", "detail": "<concrete leverage guidance for this risk %>"}},
    {{"title": "Timeframe Alignment", "detail": "<which timeframes this R:R suits and why>"}}
  ],

  "confluence_checklist": [
    {{"label": "Trend Filter", "detail": "<specific condition to check>"}},
    {{"label": "Rejection Signal", "detail": "<specific condition to check, include a price zone>"}},
    {{"label": "Volume Confirmation", "detail": "<specific condition to check>"}},
    {{"label": "Macro/Flow Context", "detail": "<specific condition to check, reference Fear & Greed and news>"}},
    {{"label": "Slippage Guard", "detail": "<specific execution tip>"}}
  ],

  "risk_management_rules": [
    {{"label": "Position Sizing", "detail": "<specific % guidance>"}},
    {{"label": "Trailing Stop", "detail": "<specific price levels for breakeven move and trailing>"}},
    {{"label": "News Buffer", "detail": "<specific guidance around news events>"}},
    {{"label": "Correlation Check", "detail": "<what correlated assets/markets to watch>"}}
  ],

  "final_verdict": "<2-3 sentence closing verdict on the setup's quality and what must be validated before execution>",

  "full_report": "<2-4 sentences expanding on PERCEIVE/NEWS/DECIDE/EXECUTE/RISK/MEMORY
   in plain prose, as a fallback narrative if structured fields can't be displayed>"
}}
"""

        # =====================
        # FIX 12 - CALL QWEN (or demo stub)
        # =====================

        structured = None

        if demo:

            ai_direction = technical_direction
            ai_confidence = technical_confidence
            ai_reasoning = (
                f"Demo Mode: technical-only signal. EMA trend, momentum, and "
                f"candle strength suggest {technical_direction}."
            )
            report = (
                f"Demo Mode: technical-only breakdown for {symbol}. RSI(14) reads {round(rsi,1)}, "
                f"volatility is {round(volatility,3)}%, volume is {volume_trend.lower()}, and 5-candle "
                f"momentum is {round(momentum,2)}%. This combination points to {ai_direction}. "
                f"Turn off Demo Mode for full Qwen AI reasoning over news and sentiment."
            )

        else:

            try:
                response = client.chat.completions.create(
                    model="qwen3.6-flash",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an autonomous crypto trading agent. You always respond with strictly valid JSON only."
                        },
                        {
                            "role": "user",
                            "content": agent_prompt
                        }
                    ]
                )

                raw_report = response.choices[0].message.content.strip()

                # Strip accidental markdown fences if the model adds them anyway
                if raw_report.startswith("```"):
                    raw_report = raw_report.strip("`")
                    if raw_report.lower().startswith("json"):
                        raw_report = raw_report[4:].strip()

                parsed = json.loads(raw_report)

                ai_direction = parsed.get("direction", technical_direction).upper()
                ai_confidence = int(parsed.get("confidence", technical_confidence))
                ai_reasoning = parsed.get("reasoning", "No reasoning provided.")
                report = parsed.get("full_report", ai_reasoning)
                structured = parsed

            except Exception as e:
                # If Qwen fails or returns bad JSON, fall back to the technical signal
                # rather than crashing the agent.
                ai_direction = technical_direction
                ai_confidence = technical_confidence
                ai_reasoning = (
                    f"⚠️ Qwen AI call failed ({e}). Fell back to technical-only signal: "
                    f"{technical_direction} ({technical_confidence}%)."
                )
                report = ai_reasoning

        # Normalize direction/signal/SL-TP based on the FINAL decision
        if ai_direction == "LONG":
            direction = "LONG 📈"
            signal = "BUY 🟢"
            sl = round(price * 0.98, 2)
            tp = round(price * 1.04, 2)
        elif ai_direction == "SHORT":
            direction = "SHORT 📉"
            signal = "SELL 🔴"
            sl = round(price * 1.02, 2)
            tp = round(price * 0.96, 2)
        else:
            direction = "WAIT ⏳"
            signal = "HOLD 🟡"
            sl = round(price * 0.99, 2)
            tp = round(price * 1.01, 2)

        confidence = f"{ai_confidence}%"

        # =====================
        # FIX 13 - STRUCTURED REPORT DATA (tables/checklists like the original report)
        # When Qwen didn't return structured fields (demo mode, or fallback), build
        # an equivalent structure here from real computed numbers - never placeholders.
        # =====================

        risk_amount = abs(sl - price)
        reward_amount = abs(tp - price)
        rr_ratio = (reward_amount / risk_amount) if risk_amount else 0
        breakeven_win_rate = (1 / (1 + rr_ratio)) * 100 if rr_ratio else 50

        if structured is None:
            structured = {
                "summary": f"Here's a systematic breakdown of your {symbol} {ai_direction} setup based on current conditions.",
                "trade_metrics": {
                    "risk_reward_ratio": f"1 : {rr_ratio:.2f}",
                    "risk_reward_note": "Mathematically optimal for consistent edge" if rr_ratio >= 1.5 else "Tight reward relative to risk - size accordingly",
                    "breakeven_win_rate": f"{breakeven_win_rate:.2f}%",
                    "breakeven_note": f"Profitable if actual win rate > {breakeven_win_rate:.1f}%",
                    "risk_per_unit": f"{(risk_amount / price * 100):.2f}%",
                    "risk_per_unit_note": "Disciplined; aligns with standard swing/position sizing"
                },
                "structural_analysis": [
                    {"title": "Invalidation Zone", "detail": f"{'>' if ai_direction == 'SHORT' else '<'}{sl} (~{(risk_amount/price*100):.1f}%). If price closes beyond this level, the {ai_direction.lower()} thesis is structurally broken."},
                    {"title": "Profit Target Proximity", "detail": f"{tp} is the technical target. Expect possible rejection or liquidity grabs near round-number levels close to this price."},
                    {"title": "Leverage vs. Liquidation", "detail": f"With a {(risk_amount/price*100):.1f}% risk buffer, keep leverage low enough that liquidation sits well beyond {sl}. Avoid >5x unless scalping tight timeframes."},
                    {"title": "Timeframe Alignment", "detail": f"This {rr_ratio:.1f}:1 R:R suits H4/D1 swing structures. On lower timeframes, confirm the SL isn't sitting inside a high-noise liquidity zone."}
                ],
                "confluence_checklist": [
                    {"label": "Trend Filter", "detail": f"Confirm {symbol} trend direction matches {ai_direction} (EMA20 {'>' if ema20 > ema50 else '<'} EMA50)."},
                    {"label": "Rejection Signal", "detail": f"Look for confirming candle patterns or RSI divergence near {round(price,2)}."},
                    {"label": "Volume Confirmation", "detail": f"Volume is currently {volume_trend.lower()} vs its 20-period average - {'supportive' if volume_trend == 'Above Average' else 'lacks confirmation, watch closely'}."},
                    {"label": "Macro/Flow Context", "detail": f"Fear & Greed reads {fng_block}; {len(news_headlines)} relevant headline(s) found - factor sentiment into conviction."},
                    {"label": "Slippage Guard", "detail": "Place limit orders at entry/TP instead of market orders if liquidity is thin. Use OCO brackets where possible."}
                ],
                "risk_management_rules": [
                    {"label": "Position Sizing", "detail": "Risk no more than 1-2% of total capital per trade."},
                    {"label": "Trailing Stop", "detail": f"Once price moves favorably, consider trailing the stop toward breakeven near {price}, then trail behind structure."},
                    {"label": "News Buffer", "detail": "Widen stops or pause auto-execution around major macro events (CPI, FOMC, exchange-moving news)."},
                    {"label": "Correlation Check", "detail": "Monitor correlated majors (e.g. BTC/ETH) and broader market futures - divergence can cause false breaks."}
                ],
                "final_verdict": f"{'Mathematically sound' if rr_ratio >= 1.5 else 'Workable but tight'} setup with a {rr_ratio:.1f}:1 risk-reward and {(risk_amount/price*100):.1f}% downside risk. Validate against live chart structure and volume before executing.",
                "full_report": report
            }

        st.subheader(
            "🤖 Agent Decision"
        )


        a,b,c = st.columns(3)


        a.metric(
            "Direction",
            direction
        )


        b.metric(
            "Confidence",
            confidence
        )


        c.metric(
            "Signal",
            signal
        )



        x,y = st.columns(2)


        x.metric(
            "🛑 Stop Loss",
            sl
        )


        y.metric(
            "💰 Take Profit",
            tp
        )

        st.subheader(
            "📊 Market Analysis"
        )

        i1, i2, i3, i4 = st.columns(4)

        i1.metric("RSI (14)", round(rsi, 1))
        i2.metric("Volatility", f"{round(volatility, 3)}%")
        i3.metric("Volume", volume_trend)
        i4.metric("Momentum (5c)", f"{round(momentum, 2)}%")

        st.subheader(
            "😨 Fear & Greed Index"
        )

        st.info(fng_block)

        st.subheader(
            "📰 Crypto News"
        )

        if news_headlines:
            for h in news_headlines:
                st.write(f"• {h}")
        else:
            st.write("No recent relevant headlines found.")


        st.subheader(
            "📊 Market Chart"
        )


        fig = go.Figure()


        fig.add_trace(
            go.Scatter(
                y=df["close"],
                name="Price"
            )
        )


        fig.add_trace(
            go.Scatter(
                y=df["EMA20"],
                name="EMA20"
            )
        )


        fig.add_trace(
            go.Scatter(
                y=df["EMA50"],
                name="EMA50"
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



        st.subheader(
            "⚡ Agent Execution Center"
        )


        st.success(
        f"Virtual Execution Created ✅ {direction}"
    )

        st.session_state.trade_logs.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "asset": symbol,
        "decision": direction,
        "entry": price,
        "stop_loss": sl,
        "take_profit": tp,
        "confidence": confidence,
        "reasoning": ai_reasoning
    })

        save_trade_log(
            symbol,
            direction,
            price,
            sl,
            tp,
            confidence,
            ai_reasoning
        )

        st.subheader(
            "🧾 Agent Memory"
        )


        m1,m2,m3 = st.columns(3)


        m1.metric(
            "Asset",
            symbol
        )


        m2.metric(
            "Decision",
            direction
        )


        m3.metric(
            "Confidence",
            confidence
        )

        with st.expander("📜 Past decisions on this asset"):
            if past_decisions:
                for p_time, p_asset, p_decision, p_confidence, p_reasoning in past_decisions:
                    st.markdown(f"**{p_time}** — {p_decision} ({p_confidence})")
                    st.caption(p_reasoning or "No reasoning recorded.")
            else:
                st.write("No prior decisions recorded for this asset yet.")



        st.subheader(
            "🧠 Qwen AI Report"
        )

        st.write(structured.get("summary", f"Here's a breakdown of your {symbol} {ai_direction} setup."))

        st.markdown("#### 📊 Trade Metrics")

        tm = structured.get("trade_metrics", {})

        metrics_df = pd.DataFrame(
            [
                ["Entry Price", f"{price}", ""],
                ["Stop Loss", f"{sl}", f"{'+' if sl > price else '-'}{abs(round(sl - price, 2))} ({'+' if ai_direction != 'SHORT' else '-'}{(risk_amount/price*100):.2f}%)"],
                ["Take Profit", f"{tp}", f"{'+' if tp > price else '-'}{abs(round(tp - price, 2))} ({'+' if ai_direction == 'LONG' else '-'}{(reward_amount/price*100):.2f}%)"],
                ["Risk-Reward Ratio", tm.get("risk_reward_ratio", f"1 : {rr_ratio:.2f}"), tm.get("risk_reward_note", "")],
                ["Breakeven Win Rate", tm.get("breakeven_win_rate", f"{breakeven_win_rate:.2f}%"), tm.get("breakeven_note", "")],
                ["Risk per Unit", tm.get("risk_per_unit", f"{(risk_amount/price*100):.2f}%"), tm.get("risk_per_unit_note", "")],
            ],
            columns=["Parameter", "Value", "Notes"]
        )

        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        st.markdown("#### 🔍 Structural & Execution Analysis")

        for idx, item in enumerate(structured.get("structural_analysis", []), start=1):
            st.markdown(f"**{idx}. {item.get('title', '')}:** {item.get('detail', '')}")

        st.markdown("#### 🧩 Confluence Checklist Before Execution")

        for c_idx, item in enumerate(structured.get("confluence_checklist", [])):
            st.checkbox(
                f"{item.get('label', '')}: {item.get('detail', '')}",
                value=True,
                disabled=True,
                key=f"confluence_{symbol}_{c_idx}"
            )

        st.markdown("#### ⚙️ Recommended Risk Management Rules")

        for item in structured.get("risk_management_rules", []):
            st.markdown(f"- **{item.get('label', '')}:** {item.get('detail', '')}")

        st.markdown("#### 📌 Final Verdict")

        st.success(structured.get("final_verdict", report))

        st.caption("⚠️ Not financial advice. Always backtest and paper-trade new setups before live deployment.")
# ======================
# AGENT WORKFLOW CARDS
# ======================


st.markdown("## 🤖 Agent Workflow")


w1,w2,w3,w4 = st.columns(4)


with w1:

    st.markdown(
    """
<div class="card" style="text-align:center">

<h1>👁</h1>

<h3>Perceive</h3>

<p>
Scanning real-time
market data from
Bitget API
</p>

</div>
""",
    unsafe_allow_html=True
    )


with w2:

    st.markdown(
    """
<div class="card" style="text-align:center">

<h1>🧠</h1>

<h3>Decide</h3>

<p>
AI reasoning using
Alibaba Qwen model
</p>

</div>
""",
    unsafe_allow_html=True
    )


with w3:

    st.markdown(
    """
<div class="card" style="text-align:center">

<h1>⚡</h1>

<h3>Execute</h3>

<p>
Generate smart
trading actions
</p>

</div>
""",
    unsafe_allow_html=True
    )


with w4:

    st.markdown(
    """
<div class="card" style="text-align:center">

<h1>🛡</h1>

<h3>Manage Risk</h3>

<p>
Calculate SL/TP
and protect trades
</p>

</div>
""",
    unsafe_allow_html=True
    )
