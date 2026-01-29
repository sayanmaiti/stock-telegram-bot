import time
import asyncio
import yfinance as yf
from telegram import Bot

# ===== CONFIG =====
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

STOCKS = [
    "PLTR", "LMT", "BAESY", "DRS", "SNAP", "ASML", "IOSGY", "UPS",
    "TSLA", "NU", "PYPL", "AAPL", "SCCO", "MSFT", "PDD", "SOFI",
    "MCHI", "LLY", "VST", "NVO", "BRK-B", "META", "ORCL", "RKLB",
    "NVDA", "GRAB", "LYFT", "AMD", "AVGO", "TTD", "NFLX",
    "GOOGL", "UBER", "MELI", "TSM", "SIX2.DE", "AMZN", "PG"
]

DROP_LIMIT = -1.0            # alert if down 1% or more
CHECK_EVERY_SECONDS = 30     # check every 30 seconds
# ==================

bot = Bot(token=BOT_TOKEN)
alerted_today = set()

async def check_stocks():
    for symbol in STOCKS:
        try:
            data = yf.Ticker(symbol).history(period="1d")
            if data.empty:
                continue

            open_price = data["Open"].iloc[0]
            current_price = data["Close"].iloc[-1]
            change_pct = (current_price - open_price) / open_price * 100

            if change_pct <= DROP_LIMIT and symbol not in alerted_today:
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=(
                        f"🚨 {symbol} ALERT\n"
                        f"Down: {change_pct:.2f}% today\n"
                        f"Price: {current_price:.2f}"
                    )
                )
                alerted_today.add(symbol)

        except Exception as e:
            print(f"Error with {symbol}: {e}")

def reset_daily_alerts():
    alerted_today.clear()

if __name__ == "__main__":
    last_reset_day = None
    print("✅ Stock bot running")

    while True:
        today = time.strftime("%Y-%m-%d")

        if today != last_reset_day:
            reset_daily_alerts()
            last_reset_day = today

        asyncio.run(check_stocks())
        time.sleep(CHECK_EVERY_SECONDS)
