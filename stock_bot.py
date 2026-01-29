import time
import yfinance as yf
from telegram import Bot

# ===== CONFIG =====
BOT_TOKEN = "7563850022:AAFS1vmFNcE6Eeqd93I9zA1t6z59DmBJOfY"
CHAT_ID = "6654008816"

STOCKS = [
    "PLTR",
    "LMT",
    "BAESY",
    "DRS",
    "SNAP",
    "ASML",
    "IOSGY",
    "UPS",
    "TSLA",
    "NU",
    "PYPL",
    "AAPL",
    "SCCO",
    "MSFT",
    "PDD",
    "SOFI",
    "MCHI",
    "LLY",
    "VST",
    "NVO",
    "BRK-B",
    "META",
    "ORCL",
    "RKLB",
    "NVDA",
    "GRAB",
    "LYFT",
    "AMD",
    "AVGO",
    "TTD",
    "NFLX",
    "GOOGL",
    "UBER",
    "MELI",
    "TSM",
    "SIX",
    "AMZN",
    "PG"
]

DROP_LIMIT = -1.0            # alert if down 1% or more
CHECK_EVERY_SECONDS = 30     # check every 30 seconds
# ==================

bot = Bot(token=BOT_TOKEN)
alerted_today = set()

def check_stocks():
    global alerted_today

    for symbol in STOCKS:
        try:
            data = yf.Ticker(symbol).history(period="1d")
            if data.empty:
                continue

            open_price = data["Open"].iloc[0]
