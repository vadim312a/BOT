import requests
import time
import os

TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН"
OWNER_ID = 1460740609

last_update_id = 0


def execute_command(text):
    if text == "/dota":
        os.startfile("steam://rungameid/570")

    elif text == "/shutdown":
        os.system("shutdown /s /t 0")

    elif text == "/status":
        # просто ответ через Telegram
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": OWNER_ID,
                "text": "🟢 ПК работает (agent online)"
            }
        )


while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=10).json()

        for upd in r.get("result", []):
            update_id = upd["update_id"]

            if update_id <= last_update_id:
                continue

            last_update_id = update_id

            msg = upd.get("message", {})
            user_id = msg.get("from", {}).get("id")
            text = msg.get("text", "")

            if user_id != OWNER_ID:
                continue

            execute_command(text)

    except Exception as e:
        print("ERROR:", e)

    time.sleep(2)