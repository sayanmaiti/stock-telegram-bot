import time
import yfinance as yf
from telegram import Bot

# ===== CONFIG =====
BOT_TOKEN = "7563850022:AAH8eNLig8UhuCo0AlwNifRe32k6VUqyKAo"
CHAT_ID = "YOUR_CHAT_ID_HERE"

STOCKS = ["AAPL", "TSLA", "MSFT"]   # stocks you own
DROP_LIMIT = -5.0                  # alert if down 5% or more
CHECK_EVERY_SECONDS = 600           # 10 minutes
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

            open_price = data["Open"][0]
            current_price = data["Close"][-1]
            change_pct = (current_price - open_price) / open_price * 100

            key = f"{symbol}"

            if change_pct <= DROP_LIMIT and key not in alerted_today:
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=(
                        f"🚨 {symbol} ALERT\n"
                        f"Down: {change_pct:.2f}% today\n"
                        f"Price: ${current_price:.2f}"
                    )
                )
                alerted_today.add(key)

        except Exception as e:
            print(f"Error with {symbol}: {e}")

def reset_daily_alerts():
    global alerted_today
    alerted_today.clear()

if __name__ == "__main__":
    last_reset_day = None

    while True:
        today = time.strftime("%Y-%m-%d")

        if today != last_reset_day:
            reset_daily_alerts()
            last_reset_day = today

        check_stocks()
        time.sleep(CHECK_EVERY_SECONDS)
