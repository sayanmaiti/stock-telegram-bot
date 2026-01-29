import time
import asyncio
import yfinance as yf
from telegram import Bot

# ===== CONFIG =====
BOT_TOKEN = "7563850022:AAFS1vmFNcE6Eeqd93I9zA1t6z59DmBJOfY"
CHAT_ID = "6654008816"

STOCKS = [
    "PLTR", "LMT", "BAESY", "DRS", "SNAP", "ASML", "UPS",
    "TSLA", "NU", "PYPL", "AAPL", "SCCO", "MSFT", "PDD", "SOFI",
    "MCHI", "LLY", "VST", "NVO", "BRK-B", "META", "ORCL", "RKLB",
    "NVDA", "GRAB", "LYFT", "AMD", "AVGO", "TTD", "NFLX",
    "GOOGL", "UBER", "MELI", "TSM", "SIX2.DE", "AMZN", "PG"
]

ALERT_STEPS = [-2, -4, -6, -8, -10]   # progressive drop levels (%)
CHECK_EVERY_SECONDS = 30
# ==================

bot = Bot(token=BOT_TOKEN)

# symbol -> deepest step already alerted today
alerted_today = {}

async def check_stocks():
    alert_sent_in_run = False
    alert_time = time.strftime("%H:%M")

    for symbol in STOCKS:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if data.empty:
                continue

            open_price = data["Open"].iloc[0]
            current_price = data["Close"].iloc[-1]
            change_pct = (current_price - open_price) / open_price * 100

            company_name = ticker.info.get("shortName", symbol)
            last_step = alerted_today.get(symbol, 0)

            for step in ALERT_STEPS:
                if change_pct <= step and last_step > step:

                    if not alert_sent_in_run:
                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"────────── Update {alert_time} ──────────"
                        )
                        alert_sent_in_run = True

                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=(
                            f"🚨 {company_name} down {change_pct:.2f}%\n"
                            f"Crossed: {step}%\n"
                            f"Price: {open_price:.2f} → {current_price:.2f}\n"
                            f"Time: {alert_time}"
                        )
                    )

                    alerted_today[symbol] = step
                    break

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
