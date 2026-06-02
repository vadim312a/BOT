import requests
import time
import subprocess
import os

TOKEN = "8965348909:AAHmsgcYX2LhDBbGObiSVej2u7capeJI1tE"

last_update_id = 0

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=10).json()

        for upd in r.get("result", []):
            update_id = upd["update_id"]

            if update_id <= last_update_id:
                continue

            last_update_id = update_id

            if "message" not in upd:
                continue

            text = upd["message"].get("text", "")

            if text == "/shutdown":
                os.system("shutdown /s /t 0")

            elif text == "/dota":
                os.startfile("steam://rungameid/570")

    except Exception as e:
        print(e)

    time.sleep(3)